#! /usr/bin/env python3

"""
Author: Akhil Karra

This file contains classes for different models that can be run locally or
from various online APIs.
"""

import json

import requests


class LocalLlama3dot18B:
    """
    A class for the locally run Llama-3.1-8B model hosted using Ollama.
    """

    def __init__(self, model_path: str):
        self.headers = {
            "Content-Type": "application/json",
        }
        self.url = "http://localhost:11434/api/chat"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {"model": "llama3.1:latest",
                 "messages": [
                     {"role": "user", "content": prompt}
                 ],
                 "stream": False}
            ),
        )
        return response.json()["message"]["content"]
