#! /usr/bin/env python3

"""Agentomics: CentralBank Knobs Tool

Specification of a custom ResultTool for the CentralBank agent and task to
extract the update of the CentralBank on its knobs based on new conditions

Author: Akhil Karra
"""

import langroid as lr
from langroid.agent.tools.orchestration import ResultTool
from langroid.pydantic_v1 import BaseModel, Field


class ResultCentralBankKnobs(BaseModel):
    """Data structure for extracting output central bank knobs from
    CentralBank"""
    target_interest_rate: float = Field(..., description="Target Interest Rate (%)")
    securities_holdings_pc_change: float = Field(..., description="Securities Holdings Percent Change (%)")


class ResultCentralBankKnobsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultCentralBankKnobs data structure to extract
    output central bank knobs from CentralBank"""
    request: str = "result_central_bank_knobs_tool"
    purpose: str = (
        "To extract <result_central_bank_knobs> into a structured response"
    )
    result_central_bank_knobs: ResultCentralBankKnobs

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tuples that will be compiled into
        few shot examples for the CentralBank"""
        return [
            # Example for target inflation and interest rates
            ("""The interest rate goal should be 2.0%,
             the target interest rate should be at 1.5%,
             and total securities holdings should decrease by 10%.""",
             cls(result_central_bank_knobs=ResultCentralBankKnobs(
                target_interest_rate=0.015,
                securities_holdings_pc_change=-0.1
             ))),
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_central_bank_knobs)
