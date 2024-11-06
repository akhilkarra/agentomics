#! /usr/bin/env python3

"""Agentomics: BigBank Knobs Tool

Specification of a custom ResultTool for the BigBank agent and task to
extract the update of the BigBank on its knobs based on new conditions

Author: Akhil Karra
"""

import langroid as lr
from langroid.agent.tools.orchestration import ResultTool
from langroid.pydantic_v1 import BaseModel, Field


class ResultBigBankKnobs(BaseModel):
    """Data structure for extracting output big bank knobs from
    BigBank"""
    loan_to_deposit_ratio: float = Field(..., description="Loan to Deposit Ratio (%)")
    deposit_interest_rate: float = Field(..., description="Deposit Interest Rate (%)")


class ResultBigBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultBigBankKnobs data structure to extract
    output big bank knobs from BigBank"""
    request: str = "result_big_bank_knobs_tool"
    purpose: str = (
        "To extract <result_big_bank_knobs> into a structured response"
    )
    result_big_bank_knobs: ResultBigBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the BigBank"""
        return [
            # Example for loan to deposit ratio and deposit interest rate
            ("""The loan to deposit ratio should be 80%,
             and the deposit interest rate should be at 1.2%.""",
             cls(result_big_bank_knobs=ResultBigBankKnobs(
                loan_to_deposit_ratio=0.80,
                deposit_interest_rate=0.012
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_big_bank_knobs)
