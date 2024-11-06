#!  /usr/bin/env python3

"""Agentomics: Economic Variables Tool

Specification of a custom ResultTool for the EconomyAgent LLM-powered agent
and task to extract the update to the economic variables.

Author: Akhil Karra
"""

import langroid as lr
from langroid.agent.tools.orchestration import ResultTool
from langroid.pydantic_v1 import BaseModel, Field


class ResultEconVars(BaseModel):
    """Data structure for extracting output economic variables from
    EconomyAgent"""
    gdp_growth_rate: float = Field(..., description="GDP Growth Rate (% Change)")
    unemployment_rate: float = Field(..., description="Unemployment Rate (%)")
    inflation_rate: float = Field(..., description="Inflation Rate (%)")


class ResultEconVarsTool(lr.agent.ToolMessage):
    """Tool definition based on ResultEconVars data structure to extract
    output economic variables from EconomyAgent"""
    request: str = "result_econ_vars_tool"
    purpose: str = (
        "To extract <result_econ_vars> into a structured response"
    )
    result_econ_vars: ResultEconVars

    @classmethod
    def examples(cls):
        """Examples in (thought, example) tupels that will be compiled into
        few shot examples for the EconomyAgent"""
        return [
            # Positive GDP and Inflation
            ("""From my analysis, I think the GDP growth rate should be 2.7%,
             the unemployment rate should be at 14%, and the inflation rate
             should be at 2.5% for this quarter.""",
             cls(result_econ_vars=ResultEconVars(
                gdp_growth_rate=0.027,
                unemployment_rate=0.14,
                inflation_rate=0.025
             ))),
            # Negative GDP and Deflation
            ("""GDP should shrink by 5.4%. Let unemployment rise to 25%.
             We should start to see deflation at a rate of 1.4%""",
             cls(result_econ_vars=ResultEconVars(
                 gdp_growth_rate=-0.054,
                 unemployment_rate=0.25,
                 inflation_rate=-0.014
             )))
        ]

    def handle(self) -> ResultTool:
        """Take unstructured response from the LLM and call ResultTool to
        extract structured answer"""
        return ResultTool(info=self.result_econ_vars)
