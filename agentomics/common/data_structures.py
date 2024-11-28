#! /usr/bin/env python3

"""Agentomics: Common Data Structures

A library of common data structures used in economic simulations
that ensure type safety and correctness while allowing modularity
and compatibility with the Langroid multi-agent framework

Author: Akhil Karra
"""
import numpy as np
import pandas as pd
from langroid.utils.globals import GlobalState

from agentomics.common.types import NonnegPercent, Percent, TypedArray


class Knobs:
    knobs = None

class EconomicVariables(Knobs):
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
        string = ""
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                string += f"{field_value.series_name}: {str(field_value)}" + "\n"
            else:
                string += f"{field}: {str(field_value)}" + "\n"
        return string + "\n"


class CentralBankKnobs(Knobs):
    """Data structure within RecurringGlobalState to represent
    key knobs manipulated by the CentralBank which are known
    to all agents"""
    def __init__(self):
        self.interest_rate_goal = Percent(0.02,
                                          name="Interest Rate Goal (%)")
        self.target_interest_rate = TypedArray(NonnegPercent,
            series_name="Target Interest Rate (%)",
            var_name="target_interest_rate")
        self.securities_holdings_pc_change = TypedArray(
            Percent,
            series_name="Securities Holdings Percent Change (%)",
            var_name="total_securities_holdings")

    def print_subfields(self):
        string = ""
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                string += f"{field_value.series_name}: {str(field_value)}" + "\n"
            elif isinstance(field_value, Percent) and field_value.name != "":
                string += f"{field_value.name}: {str(field_value)}" + "\n"
            else:
                string += f"{field}: {str(field_value)}" + "\n"
        return string + "\n"


class BigBankKnobs(Knobs):
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
        string = ""
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                string += f"{field_value.series_name}: {str(field_value)}" + "\n"
            else:
                string += f"{field}: {str(field_value)}" + "\n"
        return string + "\n"


class SmallBankKnobs(Knobs):
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
        string = ""
        for field, field_value in self.__dict__.items():
            if isinstance(field_value, TypedArray):
                string += f"{field_value.series_name}: {str(field_value)}" + "\n"
            else:
                string += f"{field}: {str(field_value)}" + "\n"
        return string + "\n"


class ThreeBankGlobalState(GlobalState):
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
        string = ""
        for field, field_value in self.__dict__.items():
            if field != "number_of_quarters_to_simulate":
                if isinstance(field_value, (EconomicVariables, CentralBankKnobs, BigBankKnobs, SmallBankKnobs)):
                    string += f"{field}:\n"
                    string += field_value.print_subfields()  # Call the nested print_subfields method
                else:
                    string += f"{field}: {field_value}" + "\n"
        return string + "\n"

    def to_pandas_df(self) -> pd.DataFrame:
        """Take all of the series generated and put them into a Pandas
        DataFrame as columns"""
        column_names = []
        list_of_lists = []
        for _, field_value in self.__dict__.items():
            if isinstance(field_value, Knobs):
                for _, subfield_value in field_value.__dict__.items():
                    if isinstance(subfield_value, TypedArray):
                        if subfield_value.var_name is not None:
                            column_names.append(subfield_value.var_name)
                        else:
                            column_names.append("")
                        list_of_lists.append(
                            subfield_value.to_list(elementary_types=True)
                        )
        array_2d = np.array(list_of_lists).T.tolist()
        return pd.DataFrame(data=array_2d, columns=column_names)


def initialize_test_data():
    """Initial values for macroeconomic variables"""
    empty_global = ThreeBankGlobalState()
    empty_global.economic_variables.gdp_growth_rate.set_array([
        Percent(0.03),  # 3% growth
        Percent(0.025),  # 2.5% growth
        Percent(0.02),  # 2% growth
    ])

    empty_global.economic_variables.unemployment_rate.set_array([
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
    ])

    empty_global.economic_variables.inflation_rate.set_array([
        Percent(0.025),  # 2.5% inflation
        Percent(0.03),   # 3% inflation
        Percent(0.035),  # 3.5% inflation
    ])

    empty_global.central_bank_knobs.target_interest_rate.set_array([
        NonnegPercent(0.02),  # 2% target interest rate
        NonnegPercent(0.025),  # 2.5% target interest rate
        NonnegPercent(0.03)    # 3% target interest rate
    ])

    empty_global.big_bank_knobs.deposit_interest_rate.set_array([
        NonnegPercent(0.01),  # 1% deposit interest rate
        NonnegPercent(0.015),  # 1.5% deposit interest rate
        NonnegPercent(0.02)    # 2% deposit interest rate
    ])

    empty_global.big_bank_knobs.loan_to_deposit_ratio.set_array([
        NonnegPercent(0.8),  # 80% loan-to-deposit ratio
        NonnegPercent(0.75),  # 75% loan-to-deposit ratio
        NonnegPercent(0.7)    # 70% loan-to-deposit ratio
    ])

    empty_global.small_bank_knobs.consumer_loan_focus.set_array([
        NonnegPercent(0.6),  # 60% focus on consumer loans
        NonnegPercent(0.65),  # 65% focus on consumer loans
        NonnegPercent(0.7)    # 70% focus on consumer loans
    ])

    empty_global.small_bank_knobs.loans_interest_rate.set_array([
        NonnegPercent(0.04),  # 4% loans interest rate
        NonnegPercent(0.045),  # 4.5% loans interest rate
        NonnegPercent(0.05)    # 5% loans interest rate
    ])

    empty_global.central_bank_knobs.securities_holdings_pc_change.set_array([
        Percent(0.01),  # 1% increase in securities holdings
        Percent(0.015),  # 1.5% increase in securities holdings
        Percent(0.02)    # 2% increase in securities holdings
    ])

    empty_global.number_of_quarters_to_simulate = 1

    return empty_global
