#! /usr/bin/env python3

"""Three Banks Round-Based Economic Simulation

Simple Simulation of a central banking authority, a large commercial bank,
and a small commercial bank responding to a series of high inflation readings.

Author: Akhil Karra
"""
import agentomics.agents.big_bank as big_bank
import agentomics.agents.central_bank as central_bank
import agentomics.agents.economy_agent_llm as economy_agent
import agentomics.agents.small_bank as small_bank
from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.common.types import NonnegPercent, Percent
from agentomics.tools.big_bank_knobs import ResultBigBankKnobsTool
from agentomics.tools.central_bank_knobs import ResultCentralBankKnobsTool
from agentomics.tools.econ_vars_tool import ResultEconVarsTool
from agentomics.tools.small_bank_knobs import ResultSmallBankKnobsTool

MODEL_NAME = "groq/llama-3.1-70b-versatile"
# MODEL_NAME = "ollama/llama3.1:8b"


def initialize(empty_global: ThreeBankGlobalState):
    """Initial values for macroeconomic variables"""
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

    empty_global.number_of_quarters_to_simulate = 5


def main():
    model = MODEL_NAME
    globals = ThreeBankGlobalState()
    initialize(globals)
    print(globals.print_subfields())

    while globals.number_of_quarters_to_simulate > 0:
        # Have CentralBank update its knobs
        central_bank_results: ResultCentralBankKnobsTool | None = None
        while central_bank_results is None:
            central_bank_results = central_bank.run_state(model, globals)
        central_bank_new_knobs = central_bank_results.result_central_bank_knobs

        # Have BigBank update its knobs
        big_bank_results: ResultBigBankKnobsTool | None = None
        while big_bank_results is None:
            big_bank_results = big_bank.run_state(model, globals)
        big_bank_new_knobs = big_bank_results.result_big_bank_knobs

        # Have SmallBank update its knobs
        small_bank_results: ResultSmallBankKnobsTool | None = None
        while small_bank_results is None:
            small_bank_results = small_bank.run_state(model, globals)
        small_bank_new_knobs = small_bank_results.result_small_bank_knobs

        # Update the global state
        globals.central_bank_knobs.target_interest_rate.append(
            NonnegPercent(central_bank_new_knobs.target_interest_rate)
        )
        globals.central_bank_knobs.securities_holdings_pc_change.append(
            Percent(central_bank_new_knobs.securities_holdings_pc_change)
        )
        globals.big_bank_knobs.deposit_interest_rate.append(
            NonnegPercent(big_bank_new_knobs.deposit_interest_rate)
        )
        globals.big_bank_knobs.loan_to_deposit_ratio.append(
            NonnegPercent(big_bank_new_knobs.loan_to_deposit_ratio)
        )
        globals.small_bank_knobs.consumer_loan_focus.append(
            NonnegPercent(small_bank_new_knobs.consumer_loan_focus)
        )
        globals.small_bank_knobs.loans_interest_rate.append(
            NonnegPercent(small_bank_new_knobs.loans_interest_rate)
        )

        # Have EconomyAgent update the economic vars
        economy_agent_results: ResultEconVarsTool | None = None
        while economy_agent_results is None:
            economy_agent_results = economy_agent.run_state(model, globals)
        new_econ_vars = economy_agent_results.result_econ_vars

        globals.economic_variables.gdp_growth_rate.append(
            Percent(new_econ_vars.gdp_growth_rate)
        )
        globals.economic_variables.unemployment_rate.append(
            NonnegPercent(new_econ_vars.unemployment_rate)
        )
        globals.economic_variables.inflation_rate.append(
            Percent(new_econ_vars.inflation_rate)
        )

        # Go to the next round of the simulation
        globals.number_of_quarters_to_simulate -= 1
    print(globals.print_subfields())


if __name__ == "__main__":
    main()
