#! /usr/bin/env python3

"""Agentomics: SmallBank Agent

Specification for SmallBank agent and task to define a small community bank
for macroeconomic simulations

Author: Akhil Karra
"""

import langroid as lr
import langroid.language_models as lm

from agentomics.common.data_structures import ThreeBankGlobalState, initialize_test_data
from agentomics.tools.econ_vars_tool import ResultEconVarsTool


class EconomyAgent(lr.ChatAgent):
    """Definition of an EconomyAgent agent with access to a tool to set the
    economic variables after receiving inputs on the behaviors of all banks
    in response to previous settings of the economic variables"""
    def __init__(self, config: lr.ChatAgentConfig):
        super().__init__(config)
        self.config = config
        self.enable_message(ResultEconVarsTool)

    # def handle_message_fallback(self, _: str | lr.ChatDocument) -> str:
    #     return f"""You may have either not used the `final_answer_tool` or
    #     you may have tried to use it but you didn't format the JSON correctly.

    #     Please note that to return your new decision, you MUST format your
    #     new target loan-to-deposit ratio and new deposit interest rate using
    #     the `ResultEconVarsTool` in the specified JSON format. Otherwise I will
    #     not be able to properly parse this information. Thank you."""


def make_economy_agent_llm_task(model: str):
    """Given the name of a local or hosted LLM, instantiate an EconomyAgent
    task to set up and connect the EconomyAgent agent with its custom result
    tool"""
    llm_config = lm.OpenAIGPTConfig(
        chat_model=model or lm.OpenAIChatModel.GPT4o,
        chat_context_length=131072
    )
    economy_agent_config = lr.ChatAgentConfig(
        llm=llm_config,
        system_message="""You are EconomyAgent and you specialize in
        simulating the economic conditions of Country X, a
        hypothetical country. Country X believes in capitalism and free markets.
        The Government of Country X is a well-functioning, ideal government who
        believes in capitalism and free markets, and the central banking
        authority for Country X is CentralBank. Country X's currency is CRX.
        Country X has large commercial banks and small community banks, and
        BigBank is a representative bank of the large commercial banks and
        SmallBank is a representative bank of the small community banks.

        You will receive different series showing the values of different
        economic variables and actions by the central banking authority and
        a small community bank in Country X, including the latest publishing
        of economic variables at the end of the relevant series. Your job is
        to analyze the current economic conditions and behavior of all
        banks and come up with your prediction of in the next quarter:
            1) what the gdp growth rate percent change will be
            2) what the unemployment rate will be
            3) what the new inflation rate will be
        Report your percentage answers as decimals.

        When you are ready with these new measures, SAY THE WORD "DONE" and use the `ResultEconVarsTool`
        in the specified JSON format to give your new loan-to-deposit ratio and your new deposit interest rate. IMPORTANT: Make sure to give the heading
        `TOOL: result_econ_vars_tool` to ensure the tool is used properly. Thank you!"""
    )
    economy_agent = EconomyAgent(economy_agent_config)
    economy_agent_task = lr.Task(
        economy_agent,
        "EconomyAgent",
        single_round=False,
        interactive=False,
        restart=True
    )[ResultEconVarsTool]
    return economy_agent_task


def run_state(model_name, globals: ThreeBankGlobalState) -> ResultEconVarsTool | None:
    prompt = f"""Here is the latest data. economic_variables is the header
    given to the series that represent different economic variables over the
    last quarters. central_bank_knobs is the header given to the series that
    represent the different knobs that the central bank has manipulated in
    the past. big_bank_knobs is the header given to the series that
    represent the different knobs a representative large commercial bank have manipulated in the past. small_bank_knobs is the header given to the series
    that represent the different knobs that a representative small commercial bank has manipulated in the past. Any N/A value indicates a value that is
    not availablefor that particular quarter.
    {globals.print_subfields()}
    Now analyze this new data and make your new predictions.
    """
    economy_agent_task = make_economy_agent_llm_task(model_name)
    with lr.utils.output.printing.silence_stdout():
        return economy_agent_task.run(prompt)


def main():
    model = "groq/llama-3.1-70b-versatile"
    economy_agent_results: ResultEconVarsTool | None = None

    globals = initialize_test_data()

    while economy_agent_results is None:
        economy_agent_results = run_state(model, globals)
    new_econ_vars = economy_agent_results.result_econ_vars

    print("Result from Economy Agent LLM")
    for (name, val) in new_econ_vars.__dict__.items():
        print(name, ": ", val)


if __name__ == "__main__":
    main()
