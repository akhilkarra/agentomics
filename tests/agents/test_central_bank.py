import pytest
from pytest_mock import MockerFixture

from agentomics.agents.central_bank import run_state
from agentomics.tools.central_bank_knobs import (
    ResultCentralBankKnobs,
    ResultCentralBankKnobsTool,
)


@pytest.fixture
def mock_task(mocker: MockerFixture):
    # Mocking the make_big_bank_task function to avoid dependency on actual LLMs
    task_mock = mocker.MagicMock()
    task_mock.run.return_value = ResultCentralBankKnobsTool(
        result_central_bank_knobs=ResultCentralBankKnobs(
            interest_rate_goal=0.02,
            target_interest_rate=0.03,
            securities_holdings_pc_change=0.05
        )
    )
    mocker.patch("agentomics.agents.central_bank.make_central_bank_task", return_value=task_mock)
    return task_mock


def test_run_state(mock_task, mock_globals):
    # Test the run_state function with mocked global state and task
    model_name = "test-model"
    result = run_state(model_name, mock_globals)

    # Assert that the task run method was called
    mock_task.run.assert_called_once()

    # Assert the values returned from the mocked LLM response
    assert isinstance(result, ResultCentralBankKnobsTool)
    assert result.result_central_bank_knobs.interest_rate_goal == 0.02
    assert result.result_central_bank_knobs.target_interest_rate == 0.03
    assert result.result_central_bank_knobs.securities_holdings_pc_change == 0.05
