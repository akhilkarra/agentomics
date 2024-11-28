Module agentomics.agents.economy_agent_llm
==========================================
Agentomics: SmallBank Agent

Specification for SmallBank agent and task to define a small community bank
for macroeconomic simulations

Author: Akhil Karra

Functions
---------

`main()`
:

`make_economy_agent_llm_task(model: str)`
:   Given the name of a local or hosted LLM, instantiate an EconomyAgent
    task to set up and connect the EconomyAgent agent with its custom result
    tool

`run_state(model_name, globals: agentomics.common.data_structures.ThreeBankGlobalState) ‑> agentomics.tools.econ_vars_tool.ResultEconVarsTool | None`
:

Classes
-------

`EconomyAgent(config: langroid.agent.chat_agent.ChatAgentConfig)`
:   Definition of an EconomyAgent agent with access to a tool to set the
    economic variables after receiving inputs on the behaviors of all banks
    in response to previous settings of the economic variables

    Chat-mode agent initialized with task spec as the initial message sequence
    Args:
        config: settings for the agent

    ### Ancestors (in MRO)

    * langroid.agent.chat_agent.ChatAgent
    * langroid.agent.base.Agent
    * abc.ABC
