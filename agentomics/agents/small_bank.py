#! /usr/bin/env python3

"""Agentomics: SmallBank Agent

Specification for SmallBank agent and task to define a small community bank
for macroeconomic simulations

Author: Akhil Karra
"""

import langroid as lr
import langroid.language_models as lm

from agentomics.common.data_structures import ThreeBankGlobalState
from agentomics.tools.small_bank_knobs import ResultSmallBankKnobsTool


class SmallBank(lr.ChatAgent):
    """Definition of a SmallBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks"""
    def __init__(self, config: lr.ChatAgentConfig):
        super().__init__(config)
        self.config = config
        self.enable_message(ResultSmallBankKnobsTool)


def make_small_bank_task(model: str):
    """Given the name of a local or hosted LLM, instantiate a SmallBank task
    to set up and connect the SmallBank agent with its custom result tool"""
    llm_config = lm.OpenAIGPTConfig(
        chat_model=model or lm.OpenAIChatModel.GPT4o,
        chat_context_length=131072
    )
    small_bank_config = lr.ChatAgentConfig(
        llm=llm_config,
        system_message="""You are SmallBank, is a community bank
        representative of other community banks in Country X, a hypothetical
        country. Country X believes in capitalism and free markets. You are
        smart while adhering to the laws and regulations set by the Government
        of Country X (assume it is a well-functioning, ideal government who
        believes in capitalism and free markets) and CentralBank. Country X's
        currency is CRX.

        You will receive different series showing the values of different
        economic variables and actions by the central banking authority and
        a small community bank in Country X, including the latest publishing
        of economic variables at the end of the relevant series. Your job is
        to analyze the current economic conditions and behavior of the other
        banks and come up with your own game plan on:
            1) what your new loan deposit rate will be and
            2) what your new consumer loan focus will be.

        When you are ready with these new measures, say the word "DONE" and use the `ResultSmallBankKnobsTool` in the specified JSON format to give your new loan deposit rate and your new consumer loan focus. Make sure
        to give the heading `TOOL: result_small_bank_knobs_tool` to ensure the tool
        is used properly.
        """
    )
    small_bank_agent = SmallBank(small_bank_config)
    small_bank_task = lr.Task(
        small_bank_agent,
        "SmallBank",
        single_round=False,
        interactive=False,
        restart=True
    )[ResultSmallBankKnobsTool]
    return small_bank_task


def run_state(model_name, globals: ThreeBankGlobalState) -> ResultSmallBankKnobsTool | None:
    prompt = f"""Here is the latest data. economic_variables is the header
    given to the series that represent different economic variables over the
    last quarters. central_bank_knobs is the header given to the series that
    represent the different knobs that the central banking authority can
    manipulate. big_bank_knobs is the header given to the series that
    represent the different knobs that a representative large commercial
    bank can manipulate. small_bank_knobs is the header given to the series
    that represent the different knobs that you, SmallBank, have manipulated
    in the past.
    {globals.print_subfields()}
    Now analyze this new data and make your new decision on the new
    loan interest rate and consumer loan focus.
    """
    small_bank_task = make_small_bank_task(model_name)
    return small_bank_task.run(prompt)

# if __name__ == "main":
#     # run some basic tests
