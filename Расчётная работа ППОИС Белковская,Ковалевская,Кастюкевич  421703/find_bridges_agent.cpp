#include "find_bridges_agent.hpp"
#include "../keynodes/network_keynodes.hpp"

#include <sc-memory/sc_memory.hpp>
#include <sc-memory/sc_iterator.hpp>
#include <vector>
#include <map>
#include <set>
#include <unordered_map>
#include <stack>
#include <algorithm>
#include <climits>
#include <string>
#include <sstream>

using namespace std;

ScAddr FindBridgesAgent::GetActionClass() const
{
    return NetworkKeynodes::action_find_bridges;
}

static vector<ScAddr> get_neighbors(ScMemoryContext& ctx, const ScAddr& node)
{
    vector<ScAddr> neighbors;
    ScIterator5Ptr it5 = ctx.CreateIterator5(
        node,
        ScType::ConstCommonArc,
        ScType::Node,
        ScType::ConstPermPosArc,
        NetworkKeynodes::nrel_edge
    );
    
    while (it5->Next())
    {
        ScAddr neighbor = it5->Get(2);
        if (neighbor.IsValid() && neighbor != node)
        {
            neighbors.push_back(neighbor);
        }
    }
    it5 = ctx.CreateIterator5(
        ScType::Node,
        ScType::ConstCommonArc,
        node,
        ScType::ConstPermPosArc,
        NetworkKeynodes::nrel_edge
    );
    
    while (it5->Next())
    {
        ScAddr neighbor = it5->Get(0);
        if (neighbor.IsValid() && neighbor != node)
        {
            neighbors.push_back(neighbor);
        }
    }
    
    return neighbors;
}

static vector<pair<ScAddr, ScAddr>> findAllEdges(ScMemoryContext& ctx)
{
    vector<pair<ScAddr, ScAddr>> edges;
    
    ScIterator5Ptr it5 = ctx.CreateIterator5(
        ScType::Node,
        ScType::ConstCommonArc,
        ScType::Node,
        ScType::ConstPermPosArc,
        NetworkKeynodes::nrel_edge
    );
    
    while (it5->Next())
    {
        ScAddr node1 = it5->Get(0);
        ScAddr node2 = it5->Get(2);
        
        if (node1.IsValid() && node2.IsValid())
        {
            edges.push_back({node1, node2});
        }
    }
    
    return edges;
}
static ScAddr find_connecting_edge(ScMemoryContext& ctx, 
                                 const ScAddr& node1, 
                                 const ScAddr& node2)
{
    ScIterator5Ptr it5 = ctx.CreateIterator5(
        node1,
        ScType::ConstCommonArc,
        node2,
        ScType::ConstPermPosArc,
        NetworkKeynodes::nrel_edge
    );
    
    if (it5->Next())
    {
        return it5->Get(1);
    }
    
    it5 = ctx.CreateIterator5(
        node2,
        ScType::ConstCommonArc,
        node1,
        ScType::ConstPermPosArc,
        NetworkKeynodes::nrel_edge
    );
    
    if (it5->Next())
    {
        return it5->Get(1);
    }
    
    return ScAddr::Empty;
}
//самое козырное место для вопроса Татьяне Ковалевской
static void dfs_find_bridges(const ScAddr& node,
                            size_t parent_hash,
                            unordered_map<size_t, int>& visited,
                            unordered_map<size_t, int>& tin,
                            unordered_map<size_t, int>& low,
                            int& timer,
                            vector<pair<ScAddr, ScAddr>>& bridges,
                            ScMemoryContext& ctx)
{
    size_t node_hash = node.Hash();
    visited[node_hash] = 1;
    tin[node_hash] = low[node_hash] = ++timer;
    
    vector<ScAddr> neighbors = get_neighbors(ctx, node);
    
    for (const ScAddr& neighbor : neighbors)
    {
        size_t neighbor_hash = neighbor.Hash();
        
        if (neighbor_hash == parent_hash)
            continue;
        
        if (visited[neighbor_hash])
        {
            low[node_hash] = min(low[node_hash], tin[neighbor_hash]);
        }
        else
        {
            dfs_find_bridges(neighbor, node_hash, visited, tin, low, timer, bridges, ctx);
            low[node_hash] = min(low[node_hash], low[neighbor_hash]);
            
            if (low[neighbor_hash] > tin[node_hash])
            {
                bridges.push_back({node, neighbor});
            }
        }
    }
}
static double getEdgePropertyValue(ScMemoryContext& ctx, 
                                  const ScAddr& edge, 
                                  const ScAddr& property_rel)
{
    ScIterator5Ptr it5 = ctx.CreateIterator5(
        edge,
        ScType::ConstCommonArc,
        ScType::Link,  // ⬅️ Link!
        ScType::ConstPermPosArc,
        property_rel
    );
    
    if (it5->Next()) {
        ScAddr link_addr = it5->Get(2);
        std::string content;
        
        if (ctx.GetLinkContent(link_addr, content)) {
            try {
                return std::stod(content);  // string to DOUBLE
            } catch (...) {
                return 0.0;  // double
            }
        }
    }
    
    return 0.0;  // double
}

// 2. Расчёт критичности как double
static double calculateCriticalityScore(ScMemoryContext& ctx, const ScAddr& edge)
{
    double score = 0.0;  // double!
    
    // Базовая оценка
    score += 0.4;
    
    // Длина (double)
    double length = getEdgePropertyValue(ctx, edge, NetworkKeynodes::nrel_length);
    if (length > 0.0) {
        score += std::min(0.2, length / 500.0);  // 500.0 = double
    }
    
    // Стоимость (double)
    double cost = getEdgePropertyValue(ctx, edge, NetworkKeynodes::nrel_cost);
    if (cost > 0.0) {
        score += std::min(0.2, cost / 10000.0);
    }
    
    // Трафик (double)
    double traffic = getEdgePropertyValue(ctx, edge, NetworkKeynodes::nrel_traffic);
    if (traffic > 0.0) {
        score += std::min(0.2, traffic / 2000.0);
    }
    
    return std::min(1.0, score);  // double
}

static vector<vector<ScAddr>> findComponentsWithoutEdge(
    ScMemoryContext& ctx,
    const ScAddr& edge_to_remove,
    const vector<ScAddr>& all_nodes,
    const vector<pair<ScAddr, ScAddr>>& all_edges)
{
    vector<vector<ScAddr>> components;
    unordered_map<size_t, bool> visited;
    ScIterator5Ptr edge_it = ctx.CreateIterator5(
        ScType::Node,
        ScType::ConstCommonArc,
        ScType::Node,
        ScType::ConstPermPosArc,
        edge_to_remove
    );
    
    ScAddr edge_node1 = ScAddr::Empty;
    ScAddr edge_node2 = ScAddr::Empty;
    
    if (edge_it->Next())
    {
        edge_node1 = edge_it->Get(0);
        edge_node2 = edge_it->Get(2);
    }
  
    unordered_map<size_t, vector<size_t>> adjacency;
    for (const auto& edge_pair : all_edges)
    {
        bool is_edge_to_remove = false;
        
        if (edge_node1.IsValid() && edge_node2.IsValid())
        {
            if ((edge_pair.first.Hash() == edge_node1.Hash() && 
                 edge_pair.second.Hash() == edge_node2.Hash()) ||
                (edge_pair.first.Hash() == edge_node2.Hash() && 
                 edge_pair.second.Hash() == edge_node1.Hash()))
            {
                is_edge_to_remove = true;
            }
        }
        
        if (!is_edge_to_remove)
        {
            size_t hash1 = edge_pair.first.Hash();
            size_t hash2 = edge_pair.second.Hash();
            adjacency[hash1].push_back(hash2);
            adjacency[hash2].push_back(hash1);
        }
    }
    
    for (const ScAddr& node : all_nodes)
    {
        size_t node_hash = node.Hash();
        
        if (!visited[node_hash])
        {
            vector<ScAddr> component;
            stack<ScAddr> stack;
            stack.push(node);
            
            while (!stack.empty())
            {
                ScAddr current = stack.top();
                stack.pop();
                
                size_t current_hash = current.Hash();
                if (!visited[current_hash])
                {
                    visited[current_hash] = true;
                    component.push_back(current);
                    
                    // Добавляем соседей из временного графа
                    auto it = adjacency.find(current_hash);
                    if (it != adjacency.end())
                    {
                        for (size_t neighbor_hash : it->second)
                        {
                            if (!visited[neighbor_hash])
                            {
                                stack.push(ScAddr(neighbor_hash));
                            }
                        }
                    }
                }
            }
            
            if (!component.empty())
            {
                components.push_back(component);
            }
        }
    }
    
    return components;
}

static void createRedundancyRecommendation(ScMemoryContext& ctx, 
                                         const ScAddr& edge, 
                                         float criticality_score)
{
    ScAddr recommendation_class;
    
    if (criticality_score >= 0.7f)
    {
        recommendation_class = NetworkKeynodes::recommendation_immediate_redundancy;
    }
    else if (criticality_score >= 0.4f)
    {
        recommendation_class = NetworkKeynodes::recommendation_planned_redundancy;
    }
    else
    {
        recommendation_class = NetworkKeynodes::recommendation_monitoring;
    }
    
    ctx.GenerateConnector(ScType::ConstPermPosArc, recommendation_class, edge);
}


ScResult FindBridgesAgent::DoProgram(ScAction & action)
{
    m_logger.Info("FindBridgesAgent: Начало");
    try
    {
        m_logger.Info("Поиск узлов графа...");
        
        vector<ScAddr> all_nodes;
        unordered_set<size_t> unique_hashes;
        
        ScIterator3Ptr it3 = m_context.CreateIterator3(
            NetworkKeynodes::concept_node,
            ScType::ConstPermPosArc,
            ScType::Node
        );
        
        while (it3->Next())
        {
            ScAddr node = it3->Get(2);
            if (node.IsValid())
            {
                size_t hash = node.Hash();
                if (unique_hashes.find(hash) == unique_hashes.end())
                {
                    all_nodes.push_back(node);
                    unique_hashes.insert(hash);
                }
            }
        }
        
        m_logger.Info("Найдено узлов: ", all_nodes.size());
        
        if (all_nodes.empty())
        {
            m_logger.Info("Поиск узлов через рёбра...");
            
            ScIterator5Ptr it5 = m_context.CreateIterator5(
                ScType::Node,
                ScType::ConstCommonArc,
                ScType::Node,
                ScType::ConstPermPosArc,
                NetworkKeynodes::nrel_edge
            );
            
            while (it5->Next())
            {
                ScAddr node1 = it5->Get(0);
                ScAddr node2 = it5->Get(2);
                
                if (node1.IsValid())
                {
                    size_t hash1 = node1.Hash();
                    if (unique_hashes.find(hash1) == unique_hashes.end())
                    {
                        all_nodes.push_back(node1);
                        unique_hashes.insert(hash1);
                    }
                }
                
                if (node2.IsValid())
                {
                    size_t hash2 = node2.Hash();
                    if (unique_hashes.find(hash2) == unique_hashes.end())
                    {
                        all_nodes.push_back(node2);
                        unique_hashes.insert(hash2);
                    }
                }
            }
            
            m_logger.Info("Всего узлов (через рёбра): ", all_nodes.size());
        }
        
        if (all_nodes.empty())
        {
            m_logger.Warning("В базе знаний нет узлов!");
            ScStructure empty_result = m_context.GenerateStructure();
            action.SetResult(empty_result);
            return action.FinishSuccessfully();
        }
        
        m_logger.Info("Поиск рёбер графа...");
        
        vector<pair<ScAddr, ScAddr>> all_edges = findAllEdges(m_context);
        m_logger.Info("Найдено рёбер: ", all_edges.size());
        
        m_logger.Info("Запуск алгоритма поиска мостов Тарьяна...");
        
        unordered_map<size_t, int> visited, tin, low;
        int timer = 0;
        vector<pair<ScAddr, ScAddr>> found_bridges;
        
        for (const ScAddr& node : all_nodes)
        {
            size_t hash = node.Hash();
            if (!visited[hash])
            {
                dfs_find_bridges(node, ULONG_MAX, visited, tin, low, timer, 
                               found_bridges, m_context);
            }
        }
        
        m_logger.Info("Найдено мостов: ", found_bridges.size());
      
        ScStructure result = m_context.GenerateStructure();
        ScAddr result_root = m_context.GenerateNode(ScType::ConstNode);
        m_context.SetElementSystemIdentifier("bridges_analysis_result", result_root);
        
        result << result_root;
        
        if (!found_bridges.empty())
        {
            ScAddr bridges_list = m_context.GenerateNode(ScType::ConstNode);
            m_context.SetElementSystemIdentifier("identified_bridges_list", bridges_list);
            m_context.GenerateConnector(ScType::ConstPermPosArc, result_root, bridges_list);
            
            result << bridges_list;
            
            for (size_t i = 0; i < found_bridges.size(); ++i)
            {
                const auto& [node1, node2] = found_bridges[i];
                m_logger.Info("Анализ моста #", i+1, " между узлами ", 
                            node1.Hash(), " и ", node2.Hash());

                ScAddr edge = find_connecting_edge(m_context, node1, node2);
                
                if (edge.IsValid())
                {
                    ScAddr bridge_marker = m_context.GenerateConnector(
                        ScType::ConstPermPosArc,
                        NetworkKeynodes::nrel_is_bridge_result,
                        edge
                    );
                    
                    ScAddr list_entry = m_context.GenerateConnector(
                        ScType::ConstPermPosArc, bridges_list, edge);
                    m_context.GenerateConnector(
                        ScType::ConstPermPosArc,
                        NetworkKeynodes::concept_bridge,
                        edge
                    );
                    
                    vector<vector<ScAddr>> components = findComponentsWithoutEdge(
                        m_context, edge, all_nodes, all_edges);
                    
                    if (components.size() >= 2)
                    {
                        m_logger.Info("  Разделяет сеть на ", components.size(), " компонент");
                        
                        ScAddr components_node = m_context.GenerateNode(ScType::ConstNode);
                        string comp_name = "separates_into_" + to_string(components.size()) + "_parts";
                        m_context.SetElementSystemIdentifier(comp_name, components_node);
                        ScAddr connects_relation = m_context.GenerateConnector(
                            ScType::ConstPermPosArc,
                            NetworkKeynodes::nrel_connects_components,
                            components_node
                        );
                        ScAddr edge_to_components = m_context.GenerateConnector(
                            ScType::ConstCommonArc, edge, components_node
                        );
                        
                        for (size_t comp_idx = 0; comp_idx < min((size_t)2, components.size()); comp_idx++)
                        {
                            ScAddr comp_desc = m_context.GenerateNode(ScType::ConstNode);
                            string desc_name = "part_" + to_string(comp_idx+1) + 
                                              "_size_" + to_string(components[comp_idx].size());
                            m_context.SetElementSystemIdentifier(desc_name, comp_desc);
                            
                            m_context.GenerateConnector(
                                ScType::ConstPermPosArc, components_node, comp_desc);
                            
                            for (size_t node_idx = 0; node_idx < min((size_t)2, components[comp_idx].size()); node_idx++)
                            {
                                m_context.GenerateConnector(
                                    ScType::ConstPermPosArc, comp_desc, components[comp_idx][node_idx]);
                            }
                            
                            result << comp_desc;
                        }
                        
                        result << components_node << connects_relation << edge_to_components;
                    }
                    
                    float criticality = calculateCriticalityScore(m_context, edge);
                    m_logger.Info("  Оценка критичности: ", criticality);
                    
                    ScAddr criticality_node = m_context.GenerateNode(ScType::ConstNode);
                    string crit_name = "criticality_" + to_string((int)(criticality * 100)) + "%";
                    m_context.SetElementSystemIdentifier(crit_name, criticality_node);
                    
                    ScAddr crit_relation = m_context.GenerateConnector(
                        ScType::ConstPermPosArc,
                        NetworkKeynodes::nrel_criticality_score,
                        criticality_node
                    );
                    ScAddr edge_to_crit = m_context.GenerateConnector(
                        ScType::ConstCommonArc, edge, criticality_node
                    );
                    
                    createRedundancyRecommendation(m_context, edge, criticality);
                    
                    string recommendation_text;
                    if (criticality >= 0.7f)
                    {
                        recommendation_text = "НЕМЕДЛЕННОЕ РЕЗЕРВИРОВАНИЕ";
                        m_logger.Info("  Рекомендация: ", recommendation_text, " (высокая критичность)");
                    }
                    else if (criticality >= 0.4f)
                    {
                        recommendation_text = "ПЛАНОВОЕ РЕЗЕРВИРОВАНИЕ";
                        m_logger.Info("  Рекомендация: ", recommendation_text, " (средняя критичность)");
                    }
                    else
                    {
                        recommendation_text = "УСИЛЕННЫЙ МОНИТОРИНГ";
                        m_logger.Info("  Рекомендация: ", recommendation_text, " (низкая критичность)");
                    }
                    result << edge << bridge_marker << list_entry 
                           << criticality_node << crit_relation << edge_to_crit;
                }
                else
                {
                    m_logger.Warning("Не удалось найти ребро между узлами!");
                }
            }
            
            ScAddr stats_node = m_context.GenerateNode(ScType::ConstNode);
            m_context.SetElementSystemIdentifier("analysis_statistics", stats_node);
            ScAddr bridges_count = m_context.GenerateNode(ScType::ConstNode);
            string bridges_str = "total_bridges_" + to_string(found_bridges.size());
            m_context.SetElementSystemIdentifier(bridges_str, bridges_count);
            m_context.GenerateConnector(ScType::ConstPermPosArc, stats_node, bridges_count);
            ScAddr nodes_count = m_context.GenerateNode(ScType::ConstNode);
            string nodes_str = "total_nodes_" + to_string(all_nodes.size());
            m_context.SetElementSystemIdentifier(nodes_str, nodes_count);
            m_context.GenerateConnector(ScType::ConstPermPosArc, stats_node, nodes_count);
            ScAddr edges_count = m_context.GenerateNode(ScType::ConstNode);
            string edges_str = "total_edges_" + to_string(all_edges.size());
            m_context.SetElementSystemIdentifier(edges_str, edges_count);
            m_context.GenerateConnector(ScType::ConstPermPosArc, stats_node, edges_count);
            
            m_context.GenerateConnector(ScType::ConstPermPosArc, result_root, stats_node);
            
            result << stats_node << bridges_count << nodes_count << edges_count;
        }
        else
        {
            m_logger.Info("Мосты не найдены - сеть устойчива!");
            ScAddr no_bridges = m_context.GenerateNode(ScType::ConstNode);
            // ИСПРАВЛЕНО
            m_context.SetElementSystemIdentifier("no_bridges_network_resilient", no_bridges);
            m_context.GenerateConnector(ScType::ConstPermPosArc, result_root, no_bridges);
            result << no_bridges;
        }
        
        m_logger.Info("========================================");
        m_logger.Info("АНАЛИЗ ЗАВЕРШЕН УСПЕШНО");
        m_logger.Info("Узлов проанализировано: ", all_nodes.size());
        m_logger.Info("Рёбер проанализировано: ", all_edges.size());
        m_logger.Info("Мостов обнаружено: ", found_bridges.size());
        m_logger.Info("========================================");
        
        action.SetResult(result);
        return action.FinishSuccessfully();
    }
    catch (const exception& e)
    {
        m_logger.Error("Ошибка в FindBridgesAgent: ", e.what());
        return action.FinishWithError();
    }
}
