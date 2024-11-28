Module agentomics.tools.central_bank_knobs
==========================================
Agentomics: CentralBank Knobs Tool

Specification of a custom ResultTool for the CentralBank agent and task to
extract the update of the CentralBank on its knobs based on new conditions

Author: Akhil Karra

Classes
-------

`ResultCentralBankKnobs(**data: Any)`
:   Data structure for extracting output central bank knobs from
    CentralBank

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `interest_rate_goal: float`
    :

    `securities_holdings_pc_change: float`
    :

    `target_interest_rate: float`
    :

`ResultCentralBankKnobsTool(**data: Any)`
:   Tool definition based on ResultCentralBankKnobs data structure to extract
    output central bank knobs from CentralBank

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * langroid.agent.tool_message.ToolMessage
    * abc.ABC
    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `purpose: str`
    :

    `request: str`
    :

    `result_central_bank_knobs: agentomics.tools.central_bank_knobs.ResultCentralBankKnobs`
    :

    ### Static methods

    `examples()`
    :   Examples in (thought, example) tuples that will be compiled into
        few shot examples for the CentralBank

    ### Methods

    `handle(self) ‑> langroid.agent.tools.orchestration.ResultTool`
    :   Take unstructured response from the LLM and call ResultTool to
        extract structured answer
