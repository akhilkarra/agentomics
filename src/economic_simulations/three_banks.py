#! /usr/bin/env python3

"""Simple Simulation of a central banking authority, a large commercial bank,
and a small commercial bank responding to a series of high inflation readings.

Author: Akhil Karra
"""
from dataclasses import dataclass

import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import ResultTool
from langroid.pydantic_v1 import BaseModel, Field
from langroid.utils.globals import GlobalState

llm_config = lr.ChatAgentConfig(
    llm=lm.OpenAIGPTConfig(
        chat_model="ollama/llama3.1:8b",
        chat_context_length=131072
    )
)


class TypedArray:
    """Custom array datatype that typechecks every element added or set"""
    def __init__(self, type_check, series_name: str | None = None, var_name: str | None = None):
        self.type_check = type_check
        self.series_name: str | None = series_name
        self.var_name: str | None = var_name
        self._array = []

    def _type_check(self, item):
        if not isinstance(item, self.type_check):
            raise TypeError(f"Item must be of type {self.type_check.__name__}")

    def append(self, item):
        self._type_check(item)
        self._array.append(item)

    def set_array(self, L: list):
        map(self._type_check, L)
        self._array = L

    def to_list(self):
        return self._array

    def __getitem__(self, index):
        if isinstance(index, slice):
            return TypedArray(self.type_check, self._array[index])
        return self._array[index]

    def __setitem__(self, index, item):
        self._type_check(item)
        self._array[index] = item

    def __add__(self, other):
        if not isinstance(other, TypedArray):
            raise TypeError("Can only concatenate with another TypedArray")
        # Check that all items in the other list are of the correct type
        map(self._type_check, other)
        # Return a new TypedArray with the combined items
        new_list = TypedArray(self.type_check)
        new_list._array = self._array + other._array
        return new_list

    def __eq__(self, other):
        if isinstance(other, list):
            return self._array == other
        if isinstance(other, TypedArray):
            return self._array == other._array
        return NotImplemented  # For unsupported types

    def __bool__(self):
        return bool(self._array)

    def __len__(self):
        return len(self._array)

    def __repr__(self):
        return repr(self._array)

    def print_subfields(self):
        print(f"{self.var_name} ({self.series_name}):")
        for item in self._array:
            print(f"  - {item}")


@dataclass(frozen=True)
class NonnegFloat:
    """Custom nonnegative float datatype to ensure that LLMs return
    reasonable nonnegative values to the recurring global state"""
    value: float

    def __post_init__(self):
        if self.value < 0.0:
            raise ValueError("Floating point number must be nonnegative")


@dataclass(frozen=True)
class Percent:
    """Custom percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state."""
    value: float
    name: str | None = None

    def __post_init__(self):
        if not (0.0 <= abs(self.value) <= 1.0):
            raise ValueError("Invalid percentage input")


@dataclass(frozen=True)
class NonnegPercent:
    """Custom nonnegative percent datatype to ensure that LLMs return reasonable
    percentage values to the recurring global state."""
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError("Invalid nonnegative percentage input")


class EconomicVariables:
    """Data structure within RecurringGlobalState to represent
    key economic variables shared with all agents"""
    def __init__(self):
        self.gdp_growth_rate = TypedArray(
            Percent,
            series_name="GDP Growth Rate (% Change)",
            var_name="gdp_growth_rate")
        self.unemployment_rate = TypedArray(
            NonnegPercent,
            series_name="Unemployment Rate (%)",
            var_name="unemployment_rate")
        self.inflation_rate = TypedArray(
            Percent,
            series_name="Inflation Rate (%)",
            var_name="inflation_rate")

    def print_subfields(self):
        print("EconomicVariables Fields:")
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                field_value.print_subfields()
            else:
                print(f"{field}: {field_value}")
        print()  # Add a new line for better readability


class ResultEconVars(BaseModel):
    """Data structure for extracting output economic variables from
    EconomyAgent"""
    gdp_growth_rate: float = Field(..., description="GDP Growth Rate (% Change)")
    unemployment_rate: float = Field(..., description="Unemployment Rate (%)")
    inflation_rate: float = Field(..., description="Inflation Rate (%)")


class ResultEconVarsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultEconVars data structure to extract
    output economic variables from EconomyAgent"""
    request: str = "result_econ_vars_tool"
    purpose: str = (
        "To extract <result_econ_vars> into a structured response"
    )
    result_econ_vars: ResultEconVars

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tupels that will be compiled into
        few shot examples for the EconomyAgent"""
        return [
            # Positive GDP and Inflation
            ("""From my analysis, I think the GDP growth rate should be 2.7%,
             the unemployment rate should be at 14%, and the inflation rate
             should be at 2.5% for this quarter.""",
             cls(result_econ_vars=ResultEconVars(
                gdp_growth_rate=0.027,
                unemployment_rate=0.14,
                inflation_rate=0.025
             ))),
            # Negative GDP and Deflation
            ("""GDP should shrink by 5.4%. Let unemployment rise to 25%.
             We should start to see deflation at a rate of 1.4%""",
             cls(result_econ_vars=ResultEconVars(
                 gdp_growth_rate=-0.054,
                 unemployment_rate=0.25,
                 inflation_rate=-0.014
             )))
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_econ_vars)


class CentralBankKnobs:
    """Data structure within RecurringGlobalState to represent
    key knobs manipulated by the CentralBank which are known
    to all agents"""
    def __init__(self):
        self.target_inflation_rate = Percent(0.02,
                                             name="Target Inflation Rate (%)")
        self.target_interest_rate = TypedArray(NonnegPercent,
            series_name="Target Interest Rate (%)",
            var_name="target_interest_rate")
        self.total_securities_holdings = TypedArray(
            NonnegFloat,
            series_name="Total Securities Holdings (CUR)",
            var_name="total_securities_holdings")

    def print_subfields(self):
        print("CentralBankKnobs Fields:")
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                field_value.print_subfields()
            else:
                print(f"{field}: {field_value}")
        print()


class ResultCentralBankKnobs(BaseModel):
    """Data structure for extracting output central bank knobs from
    CentralBank"""
    target_inflation_rate: float = Field(..., description="Target Inflation Rate (%)")
    target_interest_rate: float = Field(..., description="Target Interest Rate (%)")
    total_securities_holdings: float = Field(..., description="Total Securities Holdings (CUR)")


class ResultCentralBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultCentralBankKnobs data structure to extract
    output central bank knobs from CentralBank"""
    request: str = "result_central_bank_knobs_tool"
    purpose: str = (
        "To extract <result_central_bank_knobs> into a structured response"
    )
    result_central_bank_knobs: ResultCentralBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the CentralBank"""
        return [
            # Example for target inflation and interest rates
            ("""The target inflation rate should be 2.0%,
             the target interest rate should be at 1.5%,
             and total securities holdings should be 100 million CUR.""",
             cls(result_central_bank_knobs=ResultCentralBankKnobs(
                target_inflation_rate=0.02,
                target_interest_rate=0.015,
                total_securities_holdings=100000000.0
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_central_bank_knobs)


class BigBankKnobs:
    """Data structure within RecurringGlobalState to represent
    key knobs manipulated by the BigBank large commercial bank
    which are known to all agents"""
    def __init__(self):
        self.loan_to_deposit_ratio = TypedArray(
            NonnegPercent,
            series_name="Loan to Deposit Ratio (%)",
            var_name="loan_to_deposit_ratio")
        self.deposit_interest_rate = TypedArray(
            NonnegPercent,
            series_name="Deposit Interest Rate (%)",
            var_name="deposit_interest_rate")

    def print_subfields(self):
        print("BigBankKnobs Fields:")
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                field_value.print_subfields()
            else:
                print(f"{field}: {field_value}")
        print()


class ResultBigBankKnobs(BaseModel):
    """Data structure for extracting output big bank knobs from
    BigBank"""
    loan_to_deposit_ratio: float = Field(..., description="Loan to Deposit Ratio (%)")
    deposit_interest_rate: float = Field(..., description="Deposit Interest Rate (%)")


class ResultBigBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultBigBankKnobs data structure to extract
    output big bank knobs from BigBank"""
    request: str = "result_big_bank_knobs_tool"
    purpose: str = (
        "To extract <result_big_bank_knobs> into a structured response"
    )
    result_big_bank_knobs: ResultBigBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the BigBank"""
        return [
            # Example for loan to deposit ratio and deposit interest rate
            ("""The loan to deposit ratio should be 80%,
             and the deposit interest rate should be at 1.2%.""",
             cls(result_big_bank_knobs=ResultBigBankKnobs(
                loan_to_deposit_ratio=0.80,
                deposit_interest_rate=0.012
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_big_bank_knobs)


class SmallBankKnobs:
    """Data structure within RecurringGlobalstate to represent
    key knobs manipulated by the SmallBank small community bank
    which are known to all agents"""
    def __init__(self):
        self.loans_interest_rate = TypedArray(
            NonnegPercent,
            series_name="Loans Interest Rate (%)",
            var_name="loans_interest_rate")
        self.consumer_loan_focus = TypedArray(
            NonnegPercent,
            series_name="Consumer Loan Focus (%)",
            var_name="consumer_loan_focus")

    def print_subfields(self):
        print("SmallBankKnobs Fields:")
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                field_value.print_subfields()
            else:
                print(f"{field}: {field_value}")
        print()


class ResultSmallBankKnobs(BaseModel):
    """Data structure for extracting output small bank knobs from
    SmallBank"""
    loans_interest_rate: float = Field(..., description="Loans Interest Rate (%)")
    consumer_loan_focus: float = Field(..., description="Consumer Loan Focus (%)")


class ResultSmallBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultSmallBankKnobs data structure to extract
    output small bank knobs from SmallBank"""
    request: str = "result_small_bank_knobs_tool"
    purpose: str = (
        "To extract <result_small_bank_knobs> into a structured response"
    )
    result_small_bank_knobs: ResultSmallBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the SmallBank"""
        return [
            # Example for loans interest rate and consumer loan focus
            ("""The loans interest rate should be 3.5%,
             and the consumer loan focus should be at 60%.""",
             cls(result_small_bank_knobs=ResultSmallBankKnobs(
                loans_interest_rate=0.035,
                consumer_loan_focus=0.60
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_small_bank_knobs)


class RecurringGlobalState(GlobalState):
    """Data structure representing key economic variables and
    knobs for the central bank and commercial banks"""
    class Config:
        arbitrary_types_allowed = True  # Enable arbitrary types

    economic_variables = EconomicVariables()
    central_bank_knobs = CentralBankKnobs()
    big_bank_knobs = BigBankKnobs()
    small_bank_knobs = SmallBankKnobs()
    number_of_quarters_to_simulate = 1

    def print_subfields(self):
        print("RecurringGlobalState Fields:")
        print()
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, (EconomicVariables, CentralBankKnobs, BigBankKnobs, SmallBankKnobs)):
                print(f"{field}:")
                field_value.print_subfields()  # Call the nested print_subfields method
            else:
                print(f"{field}: {field_value}")


class CentralBank:
    def __init__(self, llm_config):
        self.name = "CentralBank"
        self.sys_prompt = """You are CentralBank, a
        well-designed and comprehensive central banking authority for a
        country named Country X (which is a hypothetical country), which
        has an ideal and well-functioning government which believes in
        capitalism and free markets. Country X's currency is CUR."""
        self.agent = lr.ChatAgent(llm_config)
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            interactive=False,
            system_message=self.sys_prompt
        )


class BigBank:
    def __init__(self, llm_config):
        self.name = "BigBank"
        self.sys_prompt = """You are BigBank, a large commercial bank working
        with all kinds of clients from individuals of all economic well-beings
        to companies, corporations, and governments of various sizes and
        economic standings. You reside in a hypothetical country named
        Country X, which believes in capitalism and free markets. You are smart
        while adhering to the laws and regulations set by the Government of
        Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBank.
        Country X's currency is CUR."""
        self.agent = lr.ChatAgent(llm_config)
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            interactive=False,
            system_message=self.sys_prompt
        )


class SmallBank:
    def __init__(self, llm_config):
        self.name = "SmallBank"
        self.sys_prompt = """You are SmallBank, is a community bank
        representative of other community banks in Country X, a hypothetical
        country. Country X believes in capitalism and free markets. You are
        smart while adhering to the laws and regulations set by the Government
        of Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBank. Country X's
        currency is CUR."""
        self.agent = lr.ChatAgent(llm_config)
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            system_message=self.sys_prompt
        )


class EconomyAgent:
    def __init__(self, llm_config=None):
        if llm_config is not None:
            self.name = "EconomyAgent"
            self.sys_prompt = """You are EconomyAgent and you specialize in
            simulating the economic conditions of Country X, a
            hypothetical country. Country X believes in capitalism and free markets.
            The Government of Country X is a well-functioning, ideal government who
            believes in capitalism and free markets, and the central banking
            authority for Country X is CentralBank. Country X's currency is CUR.
            Country X has large commercial banks and small community banks, and
            BigBank is a representative bank of the large commercial banks and
            SmallBank is a representative bank of the small community banks."""
            self.agent = lr.ChatAgent(llm_config)
            self.task = lr.Task(
                self.agent,
                name=self.name,
                single_round=True,
                system_message=self.sys_prompt
            )


def initialize(empty_global):
    empty_global.economic_variables.gdp_growth_rate.set_array([
        Percent(0.03),  # 3% growth
        Percent(0.025),  # 2.5% growth
        Percent(0.02),  # 2% growth
        Percent(0.015),  # 1.5% growth
        Percent(0.01)    # 1% growth
    ])

    empty_global.economic_variables.unemployment_rate.set_array([
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.06),  # 6% unemployment
        NonnegPercent(0.07)   # 7% unemployment
    ])

    empty_global.economic_variables.inflation_rate.set_array([
        Percent(0.025),  # 2.5% inflation
        Percent(0.03),   # 3% inflation
        Percent(0.035),  # 3.5% inflation
        Percent(0.04),   # 4% inflation
        Percent(0.045)   # 4.5% inflation
    ])


def main():
    recurring_globaL_state = RecurringGlobalState()
    initialize(recurring_globaL_state)
    recurring_globaL_state.print_subfields()
    # central_bank = CentralBank(llm_config)
    # big_bank = BigBank(llm_config)
    # small_bank = SmallBank(llm_config)
    # economy_agent = EconomyAgent(llm_config=llm_config)

    # while recurring_globaL_state.number_of_quarters_to_simulate > 0:
    #     # Get response from CentralBank

    #     # Get response from BigBank

    #     # Get response from SmallBank

    #     # Get response from EconomyAgent

    #     recurring_globaL_state.number_of_quarters_to_simulate -= 1
    # recurring_globaL_state.print_subfields()


if __name__ == "__main__":
    main()
