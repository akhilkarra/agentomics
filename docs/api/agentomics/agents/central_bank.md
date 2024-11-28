Module agentomics.agents.central_bank
=====================================
Agentomics: CentralBank Agent

Specification for a CentralBank agent and task to define a central banking
authority of a fictional country for macroeconomic simulations

Functions
---------

`main()`
:

`make_central_bank_task(model: str)`
:   Given the name of a local or hosted LLM, instantiate a CentralBank
    task to set up and connect the CentralBank agent with its custom result
    tool

`run_state(model_name, globals: agentomics.common.data_structures.ThreeBankGlobalState) ‑> agentomics.tools.central_bank_knobs.ResultCentralBankKnobsTool | None`
:

Classes
-------

`CentralBank(config: langroid.agent.chat_agent.ChatAgentConfig)`
:   Definition of a CentralBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks

    Chat-mode agent initialized with task spec as the initial message sequence
    Args:
        config: settings for the agent

    ### Ancestors (in MRO)

    * langroid.agent.chat_agent.ChatAgent
    * langroid.agent.base.Agent
    * abc.ABC
