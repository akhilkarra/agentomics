Module agentomics.agents.small_bank
===================================
Agentomics: SmallBank Agent

Specification for SmallBank agent and task to define a small community bank
for macroeconomic simulations

Author: Akhil Karra

Functions
---------

`main()`
:

`make_small_bank_task(model: str)`
:   Given the name of a local or hosted LLM, instantiate a SmallBank task
    to set up and connect the SmallBank agent with its custom result tool

`run_state(model_name, globals: agentomics.common.data_structures.ThreeBankGlobalState) ‑> agentomics.tools.small_bank_knobs.ResultSmallBankKnobsTool | None`
:

Classes
-------

`SmallBank(config: langroid.agent.chat_agent.ChatAgentConfig)`
:   Definition of a SmallBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks

    Chat-mode agent initialized with task spec as the initial message sequence
    Args:
        config: settings for the agent

    ### Ancestors (in MRO)

    * langroid.agent.chat_agent.ChatAgent
    * langroid.agent.base.Agent
    * abc.ABC
