Module agentomics.tools.small_bank_knobs
========================================
Agentomics: SmallBank Knobs Tool

Specification of a custom ResultTool for the SmallBank agent and task to
extract the update of the SmallBank on its knobs based on new conditions

Author: Akhil Karra

Classes
-------

`ResultSmallBankKnobs(**data: Any)`
:   Data structure for extracting output small bank knobs from
    SmallBank

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `consumer_loan_focus: float`
    :

    `loans_interest_rate: float`
    :

`ResultSmallBankKnobsTool(**data: Any)`
:   Tool definition based on ResultSmallBankKnobs data structure to extract
    output small bank knobs from SmallBank

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

    `result_small_bank_knobs: agentomics.tools.small_bank_knobs.ResultSmallBankKnobs`
    :

    ### Static methods

    `examples()`
    :   Examples in (thought, example) tuples that will be compiled into
        few shot examples for the SmallBank

    ### Methods

    `handle(self) ‑> langroid.agent.tools.orchestration.ResultTool`
    :   Take unstructured response from the LLM and call ResultTool to
        extract structured answer
