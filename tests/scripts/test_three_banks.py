import pytest

from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.common.types import NonnegPercent, Percent
from agentomics.utils.logging import configure_logging
from scripts.economic_simulations.three_banks import simulate_two_way

MODEL_NAME = "groq/llama-3.1-8b-instant"


def initialize_globals():
    """Initial values for macroeconomic variables"""
    globals = ThreeBankGlobalState()

    globals.economic_variables.gdp_growth_rate.set_array([
        Percent(0.03),  # 3% growth
        Percent(0.025),  # 2.5% growth
        Percent(0.02),  # 2% growth
    ])

    globals.economic_variables.unemployment_rate.set_array([
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
        NonnegPercent(0.05),  # 5% unemployment
    ])

    globals.economic_variables.inflation_rate.set_array([
        Percent(0.025),  # 2.5% inflation
        Percent(0.03),   # 3% inflation
        Percent(0.035),  # 3.5% inflation
    ])

    globals.central_bank_knobs.target_interest_rate.set_array([
        NonnegPercent(0.02),  # 2% target interest rate
        NonnegPercent(0.025),  # 2.5% target interest rate
        NonnegPercent(0.03)    # 3% target interest rate
    ])

    globals.big_bank_knobs.deposit_interest_rate.set_array([
        NonnegPercent(0.01),  # 1% deposit interest rate
        NonnegPercent(0.015),  # 1.5% deposit interest rate
        NonnegPercent(0.02)    # 2% deposit interest rate
    ])

    globals.big_bank_knobs.loan_to_deposit_ratio.set_array([
        NonnegPercent(0.8),  # 80% loan-to-deposit ratio
        NonnegPercent(0.75),  # 75% loan-to-deposit ratio
        NonnegPercent(0.7)    # 70% loan-to-deposit ratio
    ])

    globals.small_bank_knobs.consumer_loan_focus.set_array([
        NonnegPercent(0.6),  # 60% focus on consumer loans
        NonnegPercent(0.65),  # 65% focus on consumer loans
        NonnegPercent(0.7)    # 70% focus on consumer loans
    ])

    globals.small_bank_knobs.loans_interest_rate.set_array([
        NonnegPercent(0.04),  # 4% loans interest rate
        NonnegPercent(0.045),  # 4.5% loans interest rate
        NonnegPercent(0.05)    # 5% loans interest rate
    ])

    globals.central_bank_knobs.securities_holdings_pc_change.set_array([
        Percent(0.01),  # 1% increase in securities holdings
        Percent(0.015),  # 1.5% increase in securities holdings
        Percent(0.02)    # 2% increase in securities holdings
    ])

    globals.number_of_quarters_to_simulate = 1

    return globals

@pytest.fixture
def globals():
    return initialize_globals()

@pytest.mark.integration
def test_three_banks_simulation(globals):
    model = MODEL_NAME

    configure_logging(log_to_console=True, log_to_file=True)

    # Run one step of the simulation
    simulate_two_way(globals, model)

    # Validate expected output ranges
    gdp_growth = globals.economic_variables.gdp_growth_rate.to_list()[-1]
    assert 0 <= gdp_growth <= 0.1, f"Unexpected GDP growth rate: {gdp_growth}"

    inflation_rate = globals.economic_variables.inflation_rate.to_list()[-1]
    assert 0 <= inflation_rate <= 0.1, f"Unexpected inflation rate: {inflation_rate}"

    unemployment_rate = globals.economic_variables.unemployment_rate.to_list()[-1]
    assert 0 <= unemployment_rate <= 1, f"Unexpected unemployment rate: {unemployment_rate}"

    print("Test passed with expected economic variables.")
