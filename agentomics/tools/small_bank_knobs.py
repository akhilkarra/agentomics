#! /usr/bin/env python3

"""Agentomics: SmallBank Knobs Tool

Specification of a custom ResultTool for the SmallBank agent and task to
extract the update of the SmallBank on its knobs based on new conditions

Author: Akhil Karra
"""

import langroid as lr
from langroid.agent.tools.orchestration import ResultTool
from langroid.pydantic_v1 import BaseModel, Field


class ResultSmallBankKnobs(BaseModel):
    """Data structure for extracting output small bank knobs from
    SmallBank"""
    loans_interest_rate: float = Field(..., description="Loans Interest Rate (%)")
    consumer_loan_focus: float = Field(..., description="Consumer Loan Focus (%)")


class ResultSmallBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultSmallBankKnobs data structure to extract
    output small bank knobs from SmallBank"""
    request: str = "result_small_bank_knobs_tool"
    purpose: str = (
        "To extract <result_small_bank_knobs> into a structured response"
    )
    result_small_bank_knobs: ResultSmallBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the SmallBank"""
        return [
            # Example for loans interest rate and consumer loan focus
            ("""The loans interest rate should be 3.5%,
             and the consumer loan focus should be at 60%.""",
             cls(result_small_bank_knobs=ResultSmallBankKnobs(
                loans_interest_rate=0.035,
                consumer_loan_focus=0.60
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_small_bank_knobs)
