#! /usr/bin/env python3

"""Agentomics: FRED Download Utilities

Utilities to download and preprocess series from the Federal Reserve Economic Data (FRED) Database.

Author: Akhil Karra
"""

import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set up API URL and API key
FRED_API_URL = "https://api.stlouisfed.org/fred/series/observations"
FRED_API_KEY = os.getenv("FRED_API_KEY")

def get_fred_data(series_id, frequency, observation_start, observation_end, column_name):
    """
    Fetch data from FRED API for the given series ID and parameters,
    and return a DataFrame with 'date' and 'value' columns (value column renamed to column_name).

    Parameters:
    - series_id (str): FRED series ID
    - frequency (str): Data frequency ('q' for quarterly, 'm' for monthly, etc.)
    - observation_start (str): Start date in format 'YYYY-MM-DD'
    - observation_end (str): End date in format 'YYYY-MM-DD'
    - column_name (str): Desired name for the value column

    Returns:
    - pd.DataFrame: DataFrame with 'date' and 'column_name' columns
    """
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "frequency": frequency,
        "observation_start": observation_start,
        "observation_end": observation_end
    }
    response = requests.get(FRED_API_URL, params=params)
    data = response.json()

    # Check if the API call was successful
    if response.status_code != 200 or "observations" not in data:
        raise Exception(f"Failed to fetch data for series ID {series_id}. Error: {data.get('error_message', 'Unknown error')}")

    df = pd.DataFrame(data["observations"])
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df[["date", "value"]].rename(columns={"value": column_name})
    return df
