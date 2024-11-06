#! /usr/bin/env python3

"""Agentomics: BigBank Agent

Specification for BigBank agent and task to define a large commercial
bank for macroeconomic simulations

Author: Akhil Karra
"""
import langroid as lr
import langroid.language_models as lm

from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.tools.big_bank_knobs import ResultBigBankKnobsTool


class BigBank(lr.ChatAgent):
    """Definition of a BigBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks"""
    def __init__(self, config: lr.ChatAgentConfig):
        super().__init__(config)
        self.config = config
        self.enable_message(ResultBigBankKnobsTool)


def make_big_bank_task(model: str):
    """Given the name of a local or hosted LLM, instantiate a BigBank task
    to set up and connect the BigBank agent with its custom result tool"""
    llm_config = lm.OpenAIGPTConfig(
        chat_model=model or lm.OpenAIChatModel.GPT4o,
        chat_context_length=131072
    )
    central_bank_config = lr.ChatAgentConfig(
        llm=llm_config,
        system_message="""You are BigBank, a large commercial bank working
        with all kinds of clients from individuals of all economic well-beings
        to companies, corporations, and governments of various sizes and
        economic standings. You reside in a hypothetical country named
        Country X, which believes in capitalism and free markets. You are smart
        while adhering to the laws and regulations set by the Government of
        Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBank.
        Country X's currency is CRX.

        You will receive different series showing the values of different
        economic variables and actions by the central banking authority and
        a small community bank in Country X, including the latest publishing
        of economic variables at the end of the relevant series. Your job is
        to analyze the current economic conditions and behavior of the other
        banks and come up with your own game plan on:
            1) what your new loan-to-deposit ratio will be and
            2) what your new deposit interest rate will be.

        When you are ready with these new measures, say the word "DONE" and use the `ResultBigBankKnobsTool`
        in the specified JSON format to give your new loan-to-deposit ratio and your new deposit interest rate. IMPORTANT: Make sure to give the heading
        `TOOL: result_big_bank_knobs_tool` to ensure the tool is used properly.
        """
    )
    big_bank_agent = BigBank(central_bank_config)
    big_bank_task = lr.Task(
        big_bank_agent,
        "BigBank",
        single_round=False,
        interactive=False,
        restart=True
    )[ResultBigBankKnobsTool]
    return big_bank_task


def run_state(model_name, globals: ThreeBankGlobalState) -> ResultBigBankKnobsTool | None:
    prompt = f"""Here is the latest data. economic_variables is the header
    given to the series that represent different economic variables over the
    last quarters. central_bank_knobs is the header given to the series that
    represent the different knobs that the central bank has manipulated in
    the past. big_bank_knobs is the header given to the series that
    represent the different knobs you, BigBank, have manipulated in the past. small_bank_knobs is the header given to the series
    that represent the different knobs that a small commercial bank has manipulated in the past.
    {globals.print_subfields()}
    Now analyze this new data and make your new decisions.
    """
    big_bank_task = make_big_bank_task(model_name)
    return big_bank_task.run(prompt)
