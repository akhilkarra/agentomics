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
from agentomics.common.data_structures import initialize_test_data
from agentomics.common.types import NonnegPercent, Percent
from agentomics.tools.big_bank_knobs import ResultBigBankKnobsTool
from agentomics.tools.central_bank_knobs import ResultCentralBankKnobsTool
from agentomics.tools.econ_vars_tool import ResultEconVarsTool
from agentomics.tools.small_bank_knobs import ResultSmallBankKnobsTool

MODEL_NAME = "groq/llama-3.1-70b-versatile"
OUTPUT_CSV_NAME = "three_banks_output"


def simulate_three_way(globals, model, outfile=None):
    """Run the three banks simulation given the initial variables and the
    model name to run. This orchestration assumes a three-way parallelism
    between the central bank, large commercial bank, and small commercial bank"""
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

        # Update the banks' global states
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

        # Update the global economic variables
        globals.economic_variables.gdp_growth_rate.append(
            Percent(new_econ_vars.gdp_growth_rate)
        )
        globals.economic_variables.unemployment_rate.append(
            NonnegPercent(new_econ_vars.unemployment_rate)
        )
        globals.economic_variables.inflation_rate.append(
            Percent(new_econ_vars.inflation_rate)
        )
        globals.number_of_quarters_to_simulate -= 1

        if outfile is not None:
            globals_pd = globals.to_pandas_df()
            globals_pd.to_csv(outfile)


def simulate_two_way(globals, model, outfile=None):
    """Run the three banks simulation given the initial variables and the
    model name to run. This orchestration assumes that the central bank makes
    its decisions first and then a two-way parallelism occurs between the large
    commercial bank and small commercial bank"""
    while globals.number_of_quarters_to_simulate > 0:
        # Have CentralBank update its knobs
        central_bank_results: ResultCentralBankKnobsTool | None = None
        while central_bank_results is None:
            central_bank_results = central_bank.run_state(model, globals)
        central_bank_new_knobs = central_bank_results.result_central_bank_knobs

        # Update the central bank's global states
        globals.central_bank_knobs.target_interest_rate.append(
            NonnegPercent(central_bank_new_knobs.target_interest_rate)
        )
        globals.central_bank_knobs.securities_holdings_pc_change.append(
            Percent(central_bank_new_knobs.securities_holdings_pc_change)
        )

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

        # Update the global economic variables
        globals.economic_variables.gdp_growth_rate.append(
            Percent(new_econ_vars.gdp_growth_rate)
        )
        globals.economic_variables.unemployment_rate.append(
            NonnegPercent(new_econ_vars.unemployment_rate)
        )
        globals.economic_variables.inflation_rate.append(
            Percent(new_econ_vars.inflation_rate)
        )
        globals.number_of_quarters_to_simulate -= 1

        if outfile is not None:
            globals_pd = globals.to_pandas_df()
            globals_pd.to_csv(outfile)


def main():
    model = MODEL_NAME
    globals = initialize_test_data()

    print(globals.print_subfields())

    simulate_three_way(globals, model)

    globals_pd = globals.to_pandas_df()
    globals_pd.to_csv(f"output/{OUTPUT_CSV_NAME}.csv")

    print(globals.print_subfields())


if __name__ == "__main__":
    main()
