Module agentomics.tools.big_bank_knobs
======================================
Agentomics: BigBank Knobs Tool

Specification of a custom ResultTool for the BigBank agent and task to
extract the update of the BigBank on its knobs based on new conditions

Author: Akhil Karra

Classes
-------

`ResultBigBankKnobs(**data: Any)`
:   Data structure for extracting output big bank knobs from
    BigBank

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `deposit_interest_rate: float`
    :

    `loan_to_deposit_ratio: float`
    :

`ResultBigBankKnobsTool(**data: Any)`
:   Tool definition based on ResultBigBankKnobs data structure to extract
    output big bank knobs from BigBank

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

    `result_big_bank_knobs: agentomics.tools.big_bank_knobs.ResultBigBankKnobs`
    :

    ### Static methods

    `examples()`
    :   Examples in (thought, example) tuples that will be compiled into
        few shot examples for the BigBank

    ### Methods

    `handle(self) ‑> langroid.agent.tools.orchestration.ResultTool`
    :   Take unstructured response from the LLM and call ResultTool to
        extract structured answer
