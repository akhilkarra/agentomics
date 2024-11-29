import pandas as pd
import pytest

from agentomics.utils.fred_download import get_fred_data


@pytest.mark.integration
def test_get_fred_data():
    series_id = "GDP"
    frequency = "q"
    observation_start = "2020-01-01"
    observation_end = "2020-12-31"
    column_name = "Gross Domestic Product"

    df = get_fred_data(
        series_id=series_id,
        frequency=frequency,
        observation_start=observation_start,
        observation_end=observation_end,
        column_name=column_name
    )

    # Check that the DataFrame is not empty
    assert not df.empty, "The DataFrame is empty."

    # Check that the DataFrame has the expected columns
    expected_columns = ["date", column_name]
    assert list(df.columns) == expected_columns, f"Expected columns {expected_columns}, got {list(df.columns)}."

    # Check the 'date' column is datetime
    assert pd.api.types.is_datetime64_any_dtype(df["date"]), "'date' column is not datetime type."

    # Check the value column is numeric
    assert pd.api.types.is_numeric_dtype(df[column_name]), f"'{column_name}' column is not numeric."

    # Check that there are no missing values
    assert df.isnull().sum().sum() == 0, "DataFrame contains missing values."

    # Optionally, check the number of rows (should be 4 quarters)
    expected_rows = 4
    assert len(df) == expected_rows, f"Expected {expected_rows} rows, got {len(df)}."
