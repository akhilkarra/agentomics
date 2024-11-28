#! /usr/bin/env python3

"""Agentomics: CentralBank Agent

Specification for a CentralBank agent and task to define a central banking
authority of a fictional country for macroeconomic simulations
"""

import langroid as lr
import langroid.language_models as lm

from agentomics.common.data_structures import ThreeBankGlobalState, initialize_test_data
from agentomics.tools.central_bank_knobs import ResultCentralBankKnobsTool


class CentralBank(lr.ChatAgent):
    """Definition of a CentralBank agent with access to a tool to set its knobs
    after receiving inputs on economic conditions and behaviors on other banks"""
    def __init__(self, config: lr.ChatAgentConfig):
        super().__init__(config)
        self.config = config
        self.enable_message(ResultCentralBankKnobsTool)


def make_central_bank_task(model: str):
    """Given the name of a local or hosted LLM, instantiate a CentralBank
    task to set up and connect the CentralBank agent with its custom result
    tool"""
    llm_config = lm.OpenAIGPTConfig(
        chat_model=model or lm.OpenAIChatModel.GPT4o,
        chat_context_length=131072
    )
    central_bank_config = lr.ChatAgentConfig(
        llm=llm_config,
        system_message="""You are CentralBank, a
        well-designed and comprehensive central banking authority for a
        country named Country X (which is a hypothetical country), which
        has an ideal and well-functioning government which believes in
        capitalism and free markets. Country X's currency is CRX.

        You will receive different series showing the values of different
        economic variables and actions by the central banking authority and
        a small community bank in Country X, including the latest publishing
        of economic variables at the end of the relevant series. Your job is
        to analyze the current economic conditions and behavior of the other
        banks and come up with your own game plan on:
            1) what your new target interest rate will be and
            2) what your new percent change in  securities holdings will be
        Report your percentages in decimals, please.

        When you are ready with these new measures, say the word "DONE" and use the `ResultCentralBankKnobsTool` in the specified JSON format to give your new target interest rate and your new total securities holdings. IMPORTANT: Make sure to give the heading `TOOL: result_central_bank_knobs_tool` to ensure the tool is used properly."""
    )
    central_bank_agent = CentralBank(central_bank_config)
    central_bank_task = lr.Task(
        central_bank_agent,
        "CentralBank",
        single_round=False,
        interactive=False,
        restart=True
    )[ResultCentralBankKnobsTool]
    return central_bank_task


def run_state(model_name, globals: ThreeBankGlobalState) -> ResultCentralBankKnobsTool | None:
    prompt = f"""Here is the latest data. economic_variables is the header
    given to the series that represent different economic variables over the
    last quarters. central_bank_knobs is the header given to the series that
    represent the different knobs that, you CentralBank, have manipulated in
    the past. big_bank_knobs is the header given to the series that
    represent the different knobs that a representative large commercial
    bank can manipulate. small_bank_knobs is the header given to the series
    that represent the different knobs that a small commercial bank has manipulated in the past.
    {globals.print_subfields()}
    Now analyze this new data and make your new decision on the new target interest rate and your new total securities holdings.
    """
    central_bank_task = make_central_bank_task(model_name)
    return central_bank_task.run(prompt)


def main():
    model = "groq/llama-3.1-70b-versatile"
    central_bank_results: ResultCentralBankKnobsTool | None = None

    globals = initialize_test_data()

    while central_bank_results is None:
        central_bank_results = run_state(model, globals)
    new_central_bank_knobs = central_bank_results.result_central_bank_knobs

    print("Result from CentralBank Agent")
    for (name, val) in new_central_bank_knobs.__dict__.items():
        print(name, ":", val)


if __name__ == "__main__":
    main()
