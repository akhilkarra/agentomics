Module agentomics.common.types
==============================
Agentomics: Common Data Types

A library of commonly used data types that emulate strong runtime type-
checking to guarantee safety and correctness of simulations

Author: Akhil Karra

Classes
-------

`NonnegFloat(value: float)`
:   Custom nonnegative float datatype to ensure that LLMs return
    reasonable nonnegative values to the recurring global state

    ### Ancestors (in MRO)

    * builtins.float

    ### Class variables

    `value: float`
    :

    ### Methods

    `to_val(self)`
    :

`NonnegPercent(value: float)`
:   Custom nonnegative percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state.

    ### Ancestors (in MRO)

    * builtins.float

    ### Class variables

    `value: float`
    :

    ### Methods

    `to_val(self)`
    :

`Percent(value: float, name: str | None = None)`
:   Custom percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state.

    ### Ancestors (in MRO)

    * builtins.float

    ### Class variables

    `name: str | None`
    :

    `value: float`
    :

    ### Methods

    `to_val(self)`
    :

`TypedArray(type_check, series_name: str | None = None, var_name: str | None = None)`
:   Custom array datatype that typechecks every element added or set

    ### Methods

    `append(self, item)`
    :

    `print_subfields(self)`
    :

    `set_array(self, L: list)`
    :

    `to_list(self, elementary_types=False)`
    :
