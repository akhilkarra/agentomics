import pytest
from pytest_mock import MockerFixture

from agentomics.agents.economy_agent_llm import run_state
from agentomics.tools.econ_vars_tool import ResultEconVars, ResultEconVarsTool


@pytest.fixture
def mock_task(mocker: MockerFixture):
    # Mocking the make_big_bank_task function to avoid dependency on actual LLMs
    task_mock = mocker.MagicMock()
    task_mock.run.return_value = ResultEconVarsTool(
        result_econ_vars=ResultEconVars(
            gdp_growth_rate=0.02,
            unemployment_rate=0.03,
            inflation_rate=0.05
        )
    )
    mocker.patch("agentomics.agents.economy_agent_llm.make_economy_agent_llm_task", return_value=task_mock)
    return task_mock


def test_run_state(mock_task, mock_globals):
    # Test the run_state function with mocked global state and task
    model_name = "test-model"
    result = run_state(model_name, mock_globals)

    # Assert that the task run method was called
    mock_task.run.assert_called_once()

    # Assert the values returned from the mocked LLM response
    assert isinstance(result, ResultEconVarsTool)
    assert result.result_econ_vars.gdp_growth_rate == 0.02
    assert result.result_econ_vars.unemployment_rate == 0.03
    assert result.result_econ_vars.inflation_rate == 0.05
