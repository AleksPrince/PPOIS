#include <sc-memory/test/sc_test.hpp>
#include <sc-memory/sc_memory.hpp>
#include "../agent/find_bridges_agent.hpp"
#include "../keynodes/network_keynodes.hpp"

using AgentTest = ScMemoryTest;

// Вспомогательная функция для создания ребра
void create_edge(ScMemoryContext* ctx, ScAddr node1, ScAddr node2)
{
    ScAddr arc = ctx->GenerateConnector(ScType::ConstCommonArc, node1, node2);
    ctx->GenerateConnector(ScType::ConstPermPosArc, NetworkKeynodes::nrel_edge, arc);
}

// Вспомогательная функция для создания узла
ScAddr create_node(ScMemoryContext* ctx)
{
    ScAddr node = ctx->GenerateNode(ScType::ConstNode);
    ctx->GenerateConnector(ScType::ConstPermPosArc, 
                          NetworkKeynodes::concept_node, 
                          node);
    return node;
}

TEST_F(AgentTest, SimpleBridgeDetection)
{
    m_ctx->SubscribeAgent<FindBridgesAgent>();
    
    ScAddr nodeA = create_node(m_ctx.get());
    ScAddr nodeB = create_node(m_ctx.get());
    ScAddr nodeC = create_node(m_ctx.get());
    
    create_edge(m_ctx.get(), nodeA, nodeB);
    create_edge(m_ctx.get(), nodeB, nodeC);
    
    ScAction action = m_ctx->GenerateAction(NetworkKeynodes::action_find_bridges);
    
    EXPECT_TRUE(action.InitiateAndWait());
    EXPECT_TRUE(action.IsFinishedSuccessfully());
    
    m_ctx->UnsubscribeAgent<FindBridgesAgent>();
}

TEST_F(AgentTest, NoBridgesInTriangle)
{
    m_ctx->SubscribeAgent<FindBridgesAgent>();
    
    ScAddr nodeA = create_node(m_ctx.get());
    ScAddr nodeB = create_node(m_ctx.get());
    ScAddr nodeC = create_node(m_ctx.get());
    
    create_edge(m_ctx.get(), nodeA, nodeB);
    create_edge(m_ctx.get(), nodeB, nodeC);
    create_edge(m_ctx.get(), nodeC, nodeA);
    
    ScAction action = m_ctx->GenerateAction(NetworkKeynodes::action_find_bridges);
    
    EXPECT_TRUE(action.InitiateAndWait());
    EXPECT_TRUE(action.IsFinishedSuccessfully());
    
    m_ctx->UnsubscribeAgent<FindBridgesAgent>();
}

TEST_F(AgentTest, ComplexNetworkFromTask)
{
    m_ctx->SubscribeAgent<FindBridgesAgent>();
    
    ScAddr nodeA = create_node(m_ctx.get());
    ScAddr nodeB = create_node(m_ctx.get());
    ScAddr nodeC = create_node(m_ctx.get());
    ScAddr nodeD = create_node(m_ctx.get());
    ScAddr nodeE = create_node(m_ctx.get());
    ScAddr nodeF = create_node(m_ctx.get());
    
    // Кольцо A-B-C-D-E-F-A
    create_edge(m_ctx.get(), nodeA, nodeB);
    create_edge(m_ctx.get(), nodeB, nodeC);
    create_edge(m_ctx.get(), nodeC, nodeD);
    create_edge(m_ctx.get(), nodeD, nodeE);
    create_edge(m_ctx.get(), nodeE, nodeF);
    create_edge(m_ctx.get(), nodeF, nodeA);
    
    // Дополнительные связи B-E, C-F
    create_edge(m_ctx.get(), nodeB, nodeE);
    create_edge(m_ctx.get(), nodeC, nodeF);
    
    ScAction action = m_ctx->GenerateAction(NetworkKeynodes::action_find_bridges);
    
    EXPECT_TRUE(action.InitiateAndWait());
    EXPECT_TRUE(action.IsFinishedSuccessfully());
    
    m_ctx->UnsubscribeAgent<FindBridgesAgent>();
}
