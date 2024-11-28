Module agentomics.common.data_structures
========================================
Agentomics: Common Data Structures

A library of common data structures used in economic simulations
that ensure type safety and correctness while allowing modularity
and compatibility with the Langroid multi-agent framework

Author: Akhil Karra

Functions
---------

`initialize_test_data()`
:   Initial values for macroeconomic variables

Classes
-------

`BigBankKnobs()`
:   Data structure within RecurringGlobalState to represent
    key knobs manipulated by the BigBank large commercial bank
    which are known to all agents

    ### Ancestors (in MRO)

    * agentomics.common.data_structures.Knobs

    ### Methods

    `print_subfields(self)`
    :

`CentralBankKnobs()`
:   Data structure within RecurringGlobalState to represent
    key knobs manipulated by the CentralBank which are known
    to all agents

    ### Ancestors (in MRO)

    * agentomics.common.data_structures.Knobs

    ### Methods

    `print_subfields(self)`
    :

`EconomicVariables()`
:   Data structure within RecurringGlobalState to represent
    key economic variables shared with all agents

    ### Ancestors (in MRO)

    * agentomics.common.data_structures.Knobs

    ### Methods

    `print_subfields(self)`
    :

`Knobs()`
:

    ### Descendants

    * agentomics.common.data_structures.BigBankKnobs
    * agentomics.common.data_structures.CentralBankKnobs
    * agentomics.common.data_structures.EconomicVariables
    * agentomics.common.data_structures.SmallBankKnobs

    ### Class variables

    `knobs`
    :

`SmallBankKnobs()`
:   Data structure within RecurringGlobalstate to represent
    key knobs manipulated by the SmallBank small community bank
    which are known to all agents

    ### Ancestors (in MRO)

    * agentomics.common.data_structures.Knobs

    ### Methods

    `print_subfields(self)`
    :

`ThreeBankGlobalState(**data: Any)`
:   Data structure representing key economic variables and
    knobs for the central bank and commercial banks

    Create a new model by parsing and validating input data from keyword arguments.

    Raises ValidationError if the input data cannot be parsed to form a valid model.

    ### Ancestors (in MRO)

    * langroid.utils.globals.GlobalState
    * pydantic.v1.main.BaseModel
    * pydantic.v1.utils.Representation

    ### Class variables

    `Config`
    :

    ### Methods

    `print_subfields(self)`
    :

    `to_pandas_df(self) ‑> pandas.core.frame.DataFrame`
    :   Take all of the series generated and put them into a Pandas
        DataFrame as columns
