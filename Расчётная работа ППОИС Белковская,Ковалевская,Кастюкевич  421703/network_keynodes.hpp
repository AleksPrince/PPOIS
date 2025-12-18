#pragma once
#include <sc-memory/sc_keynodes.hpp>

class NetworkKeynodes : public ScKeynodes
{
public:
    // Действие
    static inline ScKeynode const action_find_bridges{
        "action_find_bridges", ScType::ConstNodeClass};

    // Классы
    static inline ScKeynode const concept_network{
        "concept_network", ScType::ConstNodeClass};
    
    static inline ScKeynode const concept_node{
        "concept_node", ScType::ConstNodeClass};
    
    static inline ScKeynode const concept_bridge{
        "concept_bridge", ScType::ConstNodeClass};
    
    // Отношения для структуры
    static inline ScKeynode const nrel_edge{
        "nrel_edge", ScType::ConstNodeNonRole};
    
    // Отношения для свойств рёбер
    static inline ScKeynode const nrel_length{
        "nrel_length", ScType::ConstNodeNonRole};
    
    static inline ScKeynode const nrel_cost{
        "nrel_cost", ScType::ConstNodeNonRole};
    
    static inline ScKeynode const nrel_traffic{
        "nrel_traffic", ScType::ConstNodeNonRole};
    
    // Отношения для результатов
    static inline ScKeynode const nrel_is_bridge_result{
        "nrel_is_bridge_result", ScType::ConstNodeNonRole};
    
    static inline ScKeynode const nrel_connects_components{
        "nrel_connects_components", ScType::ConstNodeNonRole};
    
    static inline ScKeynode const nrel_criticality_score{
        "nrel_criticality_score", ScType::ConstNodeNonRole};
    
    // Классы рекомендаций
    static inline ScKeynode const recommendation_immediate_redundancy{
        "recommendation_immediate_redundancy", ScType::ConstNodeClass};
    
    static inline ScKeynode const recommendation_planned_redundancy{
        "recommendation_planned_redundancy", ScType::ConstNodeClass};
    
    static inline ScKeynode const recommendation_monitoring{
        "recommendation_monitoring", ScType::ConstNodeClass};
};
