import pytest
from pytest_mock import MockerFixture

from agentomics.agents.big_bank import run_state
from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.common.types import NonnegPercent, Percent
from agentomics.tools.big_bank_knobs import ResultBigBankKnobs, ResultBigBankKnobsTool


@pytest.fixture
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


@pytest.fixture
def mock_task(mocker: MockerFixture):
    # Mocking the make_big_bank_task function to avoid dependency on actual LLMs
    task_mock = mocker.MagicMock()
    task_mock.run.return_value = ResultBigBankKnobsTool(
        result_big_bank_knobs=ResultBigBankKnobs(loan_to_deposit_ratio=0.9,deposit_interest_rate=0.65)
    )
    mocker.patch("agentomics.agents.big_bank.make_big_bank_task", return_value=task_mock)
    return task_mock


def test_run_state(mock_task, mock_globals):
    # Test the run_state function with mocked global state and task
    model_name = "test-model"
    result = run_state(model_name, mock_globals)

    # Assert that the task run method was called
    mock_task.run.assert_called_once()

    # Assert the values returned from the mocked LLM response
    assert isinstance(result, ResultBigBankKnobsTool)
    assert result.result_big_bank_knobs.loan_to_deposit_ratio == 0.9
    assert result.result_big_bank_knobs.deposit_interest_rate == 0.65
