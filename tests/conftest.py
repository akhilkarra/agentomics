import pytest

from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.common.types import NonnegPercent, Percent


@pytest.fixture(scope="session")
def mock_globals():
    """Initial values for macroeconomic variables"""
    globals = ThreeBankGlobalState()

    globals.economic_variables.gdp_growth_rate.set_array([
        Percent(0.03), Percent(0.028), Percent(0.025)
    ])

    globals.economic_variables.unemployment_rate.set_array([
        Percent(0.04), Percent(0.038), Percent(0.036)
    ])

    globals.economic_variables.inflation_rate.set_array([
        Percent(0.015), Percent(0.02), Percent(0.023)
    ])

    globals.central_bank_knobs.target_interest_rate.set_array([
        Percent(0.01), Percent(0.0125), Percent(0.015)
    ])

    globals.central_bank_knobs.securities_holdings_pc_change.set_array([
        Percent(0.02), Percent(0.015), Percent(0.018)
    ])

    globals.big_bank_knobs.deposit_interest_rate.set_array([
        NonnegPercent(0.5), NonnegPercent(0.55), NonnegPercent(0.6)
    ])

    globals.big_bank_knobs.loan_to_deposit_ratio.set_array([
        NonnegPercent(0.8), NonnegPercent(0.82), NonnegPercent(0.85)
    ])

    globals.small_bank_knobs.consumer_loan_focus.set_array([
        NonnegPercent(0.75), NonnegPercent(0.78), NonnegPercent(0.8)
    ])

    globals.small_bank_knobs.loans_interest_rate.set_array([
        NonnegPercent(0.4), NonnegPercent(0.45), NonnegPercent(0.5)
    ])

    globals.number_of_quarters_to_simulate = 1

    return globals
