#include "network_module.hpp"
#include "agent/find_bridges_agent.hpp"

SC_MODULE_REGISTER(NetworkModule)
    ->Agent<FindBridgesAgent>();
