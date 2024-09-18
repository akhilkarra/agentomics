import pytest
from sentence_transformers import SentenceTransformer, util

from langroid_setup.two_agent_chat import get_config, run_chat


@pytest.fixture
def chat_config():
    return get_config()

def test_run_chat(chat_config):
    user_input = "[1, 2, 3, 4, 5]"
    expected_output = "15"
    response = run_chat(chat_config, user_input)
    assert expected_output in response

def test_run_chat_large_numbers(chat_config):
    user_input = "[13578, 2348791234, 3248579234875, 2345787394, 273849723]"
    expected_output = str(13578 + 2348791234 + 3248579234875 + 2345787394 + 273849723)
    response = run_chat(chat_config, user_input)
    assert expected_output in response

def test_run_chat_zeros(chat_config):
    user_input = "[0, 0, 0, 0, 0]"
    expected_output = "0"
    response = run_chat(chat_config, user_input)
    assert expected_output in response

def test_run_chat_negative_numbers(chat_config):
    user_input = "[-1, -2, -3, -4, -5]"
    expected_output = str(-1 - 2 - 3 - 4 - 5)
    response = run_chat(chat_config, user_input)
    assert expected_output in response

def test_run_chat_mixed_numbers(chat_config):
    user_input = "[1, -2, 3, -4, 5]"
    expected_output = str(1 - 2 + 3 - 4 + 5)
    response = run_chat(chat_config, user_input)
    assert expected_output in response

def test_run_chat_invalid_input(chat_config):
    user_input = "Invalid input"
    expected_output = "Invalid input format"
    model = SentenceTransformer("all-MiniLM-L6-v2")
    response = run_chat(chat_config, user_input)
    response_embedding = model.encode([response])
    expected_output_embedding = model.encode([expected_output])
    similarity = util.cos_sim(response_embedding, expected_output_embedding)
    assert similarity > 0.5

def test_run_chat_empty_input(chat_config):
    user_input = "[]"
    expected_output = "No numbers provided"
    model = SentenceTransformer("all-MiniLM-L6-v2")
    response = run_chat(chat_config, user_input)
    response_embedding = model.encode([response])
    expected_output_embedding = model.encode([expected_output])
    similarity = util.cos_sim(response_embedding, expected_output_embedding)
    assert similarity > 0.5

# def test_run_chat_no_input(chat_config):
#     user_input = ""
#     expected_output = "No input provided"
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     response = run_chat(chat_config, user_input)
#     response_embedding = model.encode([response])
#     expected_output_embedding = model.encode([expected_output])
#     similarity = util.cos_sim(response_embedding, expected_output_embedding)
#     assert similarity > 0.5
