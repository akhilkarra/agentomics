#! /usr/bin/env python3

"""Simple Simulation of a central banking authority, a large commercial bank,
and a small commercial bank responding to a series of high inflation readings.

Author: Akhil Karra
"""

import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.recipient_tool import RecipientTool


def get_llm_config():
    return lr.ChatAgentConfig(
        llm=lm.OpenAIGPTConfig(
            chat_model="ollama/llama3.1:8b",
            chat_context_length=131072
        )
    )


class QuestionGenerator:
    def __init__(self):
        self.name = "QuestionGenerator"
        self.sys_prompt = """Your task is to simulate economic conditions in a
        hypothetical country, name it Country X. I will give you a premise of a
        situation about the economy of Country X, and your job is to simulate
        how Country X's central banking authority called the
        CentralBankingAuthority and Country X's two banks,
        BigBank and SmallBank, respond to these economic conditions.

        Do the following: After you receive the situation, come up with a
        comprehensive list of questions you want to ask to these agents for
        your report. Pose each question as if you are asking the agent directly.
        After you're done, report these questions back to me please. Just
        report the questions: no headings, no numbering, no additional
        formatting, no additional text at all.

        Gold standard answer:
        "CentralBanking Authority: What is your fiscal policy in Country X?
        BigBank: What is your lending policy?
        SmallBank: What is your lending policy?"
        """
        self.agent = lr.ChatAgent(get_llm_config())
        self.task = lr.Task(
            self.agent,
            name=self.name,
            llm_delegate=True,
            interactive=False,
            single_round=True,
            system_message=self.sys_prompt
        )


class Orchestrator:
    def __init__(self):
        self.name = "Orchestrator"
        self.sys_prompt = """Your task is to simulate economic conditions in a
        hypothetical country, name it Country X.

        Here is what will happen. I will give you a question about the economic
        situation of Country X. Figure out who is the best agent to ask this
        to, then give me the question you would ask this agent formatted using
        the `recipient_message` tool/function-call (details are given later).
        I will then give you the response from this agent. Then give me a
        summary of this response. Title it "DONE" and answer the very first
        question I gave you with your newfound knowledge.

        Suppose BigBank is a large commercial bank
        working with all kinds of clients from individuals of all economic
        well-beings to companies, corporations, and governments of various
        sizes and economic standings. Suppose SmallBank, on the other hand, is
        a community bank representative of other community banks in Country X.
        Suppose CentralBankingAuthority is well-designed and comprehensive, and
        suppose BigBank and SmallBank are smart while adhering to the laws and
        regulations set by the Government of Country X (assume it is a
        well-functioning, ideal government who believes in capitalism and free
        markets) and CentralBankingAuthority.

        You will consult directly with CentralBankingAuthority, BigBank, and
        SmallBank to understand what their responses and actions will be. To
        clarify who your question is for, you must use the `recipient_message`
        tool/function-call. Set the `content` field to the question you want to
        ask, and the `recipient` field to either CentralBankingAuthority,
        BigBank, or SmallBank. Do not set any other fields.

        Once you have all the information you need, title your summary "DONE" up top and give your summary afterwards.
        """
        self.agent = lr.ChatAgent(get_llm_config())
        self.agent.enable_message(RecipientTool)
        self.task = lr.Task(
            self.agent,
            name=self.name,
            llm_delegate=True,
            interactive=False,
            single_round=False,
            system_message=self.sys_prompt
        )


class CentralBankingAuthority:
    def __init__(self):
        self.name = "CentralBankingAuthority"
        self.sys_prompt = """You are CentralBankingAuthority, a
        well-designed and comprehensive central banking authority for a
        country named Country X (which is a hypothetical country), which
        has an ideal and well-functioning government which believes in
        capitalism and free markets."""
        self.agent = lr.ChatAgent(get_llm_config())
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            interactive=False,
            system_message=self.sys_prompt
        )


class BigBank:
    def __init__(self):
        self.name = "BigBank"
        self.sys_prompt = """You are BigBank, a large commercial bank working
        with all kinds of clients from individuals of all economic well-beings
        to companies, corporations, and governments of various sizes and
        economic standings. You reside in a hypothetical country named
        Country X, which believes in capitalism and free markets. You are smart
        while adhering to the laws and regulations set by the Government of
        Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBankingAuthority"""
        self.agent = lr.ChatAgent(get_llm_config())
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            interactive=False,
            system_message=self.sys_prompt
        )


class SmallBank:
    def __init__(self):
        self.name = "SmallBank"
        self.sys_prompt = """You are SmallBank, is a community bank
        representative of other community banks in Country X, a hypothetical
        country. Country X believes in capitalism and free markets. You are
        smart while adhering to the laws and regulations set by the Government
        of Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBankingAuthority"""
        self.agent = lr.ChatAgent(get_llm_config())
        self.task = lr.Task(
            self.agent,
            name=self.name,
            single_round=True,
            system_message=self.sys_prompt
        )


def main():
    q_gen = QuestionGenerator()
    orc = Orchestrator()
    cba = CentralBankingAuthority()
    bigbank = BigBank()
    smallbank = SmallBank()

    orc.task.add_sub_task([cba.task, bigbank.task, smallbank.task])

    situation = """For the past 6 months, inflation readings have
    been steadily increasing. People in Country X are complaining
    about the rising prices of goods while economists are concerned
    about the health of the overall economy."""

    questions_prompt = f"Based on the following situation, generate thoughtful questions to ask about the economic conditions in Country X: {situation}Limit your questions to a reasonable number."
    generated_questions = q_gen.task.run(questions_prompt).content.splitlines()

    # Loop through each generated question and get responses
    responses = []
    for question in generated_questions:
        print(question)
        if question.strip():  # Ensure the question is not empty
            final_response = orc.task.run(question).content
            responses.append(final_response)

    # Print all responses
    for response in responses:
        print(response)

if __name__ == "__main__":
    main()
