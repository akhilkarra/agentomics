#! /usr/bin/env python3

"""Agentomics: FRED Download Utilities

Utilities to download and preprocess series from the Federal Reserve Economic Data (FRED) Database.

Author: Akhil Karra
"""

from functools import reduce

import pandas as pd


def get_longest_common_date_range(dataframes, date_column="date"):
    """
    Given a list of DataFrames with a common date column, return the longest contiguous date range where all DataFrames have entries for every date. In case there are contiguous blocks of the same size that work, this function returns the first valid block in the DataFrames.

    Parameters:
    - dataframes (list of pd.DataFrame): List of DataFrames to process.
    - date_column (str): Name of the date column in the DataFrames (default is 'date').

    Returns:
    - pd.DataFrame: DataFrame containing data for the longest common date range across all DataFrames.
    """

    # Ensure all DataFrames have the date column in datetime format
    for df in dataframes:
        df[date_column] = pd.to_datetime(df[date_column])

    # Merge all DataFrames on the date column using outer join to find missing dates
    merged_df = reduce(
        lambda left, right: pd.merge(left, right, on=date_column, how="outer"),
        dataframes
    )

    # Sort by date
    merged_df = merged_df.sort_values(by=date_column).reset_index(drop=True)

    # Identify rows without any NaNs across all data columns (excluding the date column)
    data_columns = merged_df.columns.difference([date_column])
    non_nan_mask = merged_df[data_columns].notnull().all(axis=1)

    # Create a group identifier for contiguous True blocks
    merged_df["block"] = (non_nan_mask != non_nan_mask.shift()).cumsum()

    # Filter only valid blocks where rows contain no NaNs
    valid_blocks = merged_df.loc[non_nan_mask]

    if valid_blocks.empty:
        print("No common date range found where all DataFrames have data.")
        return None

    # Find the largest contiguous block
    block_sizes = valid_blocks.groupby("block").size()
    largest_block_id = block_sizes.idxmax()

    # Extract the largest contiguous block
    largest_block = merged_df[merged_df["block"] == largest_block_id].drop(columns=["block"])

    assert not largest_block.isnull().values.any(), "Unexpected NaNs found in the largest_block DataFrame."

    return largest_block.reset_index(drop=True)
