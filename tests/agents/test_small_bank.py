from agentomics.agents.small_bank import make_small_bank_task, run_state
from agentomics.common.data_structures import ThreeBankGlobalState

MODEL_NAME = "groq/llama-3.1-70b-versatile"

def test_make_small_bank_task(mocker):
    mocker.patch("agentomics.agents.small_bank.lr.Task")
    make_small_bank_task(MODEL_NAME)
    assert mocker.mocks["agentomics.agents.small_bank.lr.Task"].called_once


def test_run_state(mocker):
    globals = ThreeBankGlobalState()
    mocker.patch("agentomics.agents.small_bank.make_small_bank_task")
    mocker.patch("agentomics.agents.small_bank.lr.Task.run")
    run_state(MODEL_NAME, globals)
    assert mocker.mocks["agentomics.agents.small_bank.make_small_bank_task"].called_once
    assert mocker.mocks["agentomics.agents.small_bank.lr.Task.run"].called_once
