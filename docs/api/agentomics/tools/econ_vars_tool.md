Module agentomics.tools.econ_vars_tool
======================================
Agentomics: Economic Variables Tool

Specification of a custom ResultTool for the EconomyAgent LLM-powered agent
and task to extract the update to the economic variables.

Author: Akhil Karra

Classes
-------

`ResultEconVars(**data: Any)`
:   Data structure for extracting output economic variables from
    EconomyAgent

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `gdp_growth_rate: float`
    :

    `inflation_rate: float`
    :

    `unemployment_rate: float`
    :

`ResultEconVarsTool(**data: Any)`
:   Tool definition based on ResultEconVars data structure to extract
    output economic variables from EconomyAgent

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

    `result_econ_vars: agentomics.tools.econ_vars_tool.ResultEconVars`
    :

    ### Static methods

    `examples()`
    :   Examples in (thought, example) tupels that will be compiled into
        few shot examples for the EconomyAgent

    ### Methods

    `handle(self) ‑> langroid.agent.tools.orchestration.ResultTool`
    :   Take unstructured response from the LLM and call ResultTool to
        extract structured answer
