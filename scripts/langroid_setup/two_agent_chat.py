#! /usr/bin/env python3

"""Simple Two-Agent Chat Example using Langroid.

Author: Akhil Karra
"""

import langroid as lr
import langroid.language_models as lm


def get_llm_config():
    return lr.ChatAgentConfig(
        llm=lm.OpenAIGPTConfig(
            chat_model="ollama/llama3.1:8b",
            chat_context_length=131072
        )
    )


def run_chat(config, user_input: str, max_rounds: (None | int) = None) -> str:
    # Setup student agent and task
    student_agent = lr.ChatAgent(config)
    student_task = lr.Task(
        student_agent,
        name="Student",
        system_message="""You will receive a list of numbers from me (the User),
        and your goal is to calculate their sum. However, you don't
        know how to add numbers. I can help you add numbers, two at a time,
        since I only know how to add pairs of numbers.

        Here is the algorithm you should follow:
        1. Take the first two numbers in the list, and remove them from the list. Example: if the list is [1, 2, 3, 4, 5], then you take 1 and 2, and the list becomes [3, 4, 5].
        2. Ask me for the sum of the two numbers.
        3. Place the sum at the front of the list. Do not forget the rest of the list. Example: if the sum is 3, then the list becomes [3, 3, 4, 5].
        4. Take the first two numbers in the new list, and remove them from the list. Example: if the list is [3, 3, 4, 5], then you take 3 and 3, and the list becomes [4, 5].
        5. Go back to step 2 unless the list is of length 1
        6. Once the list is of length 1, you have the final result

        For each question, simply ask me the sum of pairs of numbers in math notation, e.g., simply say "1 + 2" or "3 + 4" or "5 + 6" etc, and say nothing else. Do mentally keep track of each step, though.

        Once you have added all the numbers in the list, say DONE and give me
        the final sum. Nothing more, nothing less, please.""",
        llm_delegate=True,
        single_round=False,
        interactive=False,
        config=lr.TaskConfig(
            inf_loop_cycle_len=len(user_input)
        )
    )

    # Setup adder agent and task
    adder_agent = lr.ChatAgent(config)
    adder_task = lr.Task(
        adder_agent,
        name="Adder",
        system_message="""You are an expert on addition of numbers.
        When given numbers to add, simply return their sum, say nothing else.
        If no numbers are given simply respond "Respond invalid input given".
        """,
        single_round=True,
        interactive=False,
    )

    student_task.add_sub_task(adder_task)
    return student_task.run(user_input).content

def main():
    config = get_llm_config()
    user_input = "[13578, 2348791234, 3248579234875, 2345787394, 273849723]"
    final_response = run_chat(config, user_input)
    print(final_response)


if __name__ == "__main__":
    main()
