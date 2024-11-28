Module agentomics.agents.big_bank
=================================
Agentomics: BigBank Agent

Specification for BigBank agent and task to define a large commercial
bank for macroeconomic simulations

Author: Akhil Karra

Functions
---------

`main()`
:

`make_big_bank_task(model: str)`
:   Given the name of a local or hosted LLM, instantiate a BigBank task
    to set up and connect the BigBank agent with its custom result tool

`run_state(model_name, globals: agentomics.common.data_structures.ThreeBankGlobalState) ‑> agentomics.tools.big_bank_knobs.ResultBigBankKnobsTool | None`
:

Classes
-------

`BigBank(config: langroid.agent.chat_agent.ChatAgentConfig)`
:   Definition of a BigBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks

    Chat-mode agent initialized with task spec as the initial message sequence
    Args:
        config: settings for the agent

    ### Ancestors (in MRO)

    * langroid.agent.chat_agent.ChatAgent
    * langroid.agent.base.Agent
    * abc.ABC
