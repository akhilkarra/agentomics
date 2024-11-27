import pytest
from pytest_mock import MockerFixture

from agentomics.agents.big_bank import run_state
from agentomics.tools.big_bank_knobs import ResultBigBankKnobs, ResultBigBankKnobsTool


@pytest.fixture
def mock_task(mocker: MockerFixture):
    # Mocking the make_big_bank_task function to avoid dependency on actual LLMs
    task_mock = mocker.MagicMock()
    task_mock.run.return_value = ResultBigBankKnobsTool(
        result_big_bank_knobs=ResultBigBankKnobs(
            loan_to_deposit_ratio=0.9,
            deposit_interest_rate=0.65
        )
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
