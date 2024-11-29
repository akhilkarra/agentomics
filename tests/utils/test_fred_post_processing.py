import pandas as pd

from agentomics.utils.fred_post_processing import get_longest_common_date_range


def test_full_overlap():
    # Test Case: Full Overlap
    # Purpose:
    # Verify that the function correctly identifies the longest common date range
    # when all DataFrames have fully overlapping dates with no missing values.

    # Create sample dates
    dates = pd.date_range(start="2020-01-01", periods=5, freq="D")

    # Create DataFrame df1
    # Input df1:
    # | Index |       date       | A |
    # |-------|------------------|---|
    # |   0   | 2020-01-01       | 1 |
    # |   1   | 2020-01-02       | 2 |
    # |   2   | 2020-01-03       | 3 |
    # |   3   | 2020-01-04       | 4 |
    # |   4   | 2020-01-05       | 5 |
    df1 = pd.DataFrame({"date": dates, "A": [1, 2, 3, 4, 5]})

    # Create DataFrame df2
    # Input df2:
    # | Index |       date       | B  |
    # |-------|------------------|----|
    # |   0   | 2020-01-01       | 6  |
    # |   1   | 2020-01-02       | 7  |
    # |   2   | 2020-01-03       | 8  |
    # |   3   | 2020-01-04       | 9  |
    # |   4   | 2020-01-05       | 10 |
    df2 = pd.DataFrame({"date": dates, "B": [6, 7, 8, 9, 10]})

    # Create DataFrame df3
    # Input df3:
    # | Index |       date       | C   |
    # |-------|------------------|-----|
    # |   0   | 2020-01-01       | 11  |
    # |   1   | 2020-01-02       | 12  |
    # |   2   | 2020-01-03       | 13  |
    # |   3   | 2020-01-04       | 14  |
    # |   4   | 2020-01-05       | 15  |
    df3 = pd.DataFrame({"date": dates, "C": [11, 12, 13, 14, 15]})

    # Call the function with the DataFrames
    result = get_longest_common_date_range([df1, df2, df3])

    # Expected result is all dates with data from all DataFrames
    # Expected Output:
    # | Index |       date       | A | B  | C   |
    # |-------|------------------|---|----|-----|
    # |   0   | 2020-01-01       | 1 | 6  | 11  |
    # |   1   | 2020-01-02       | 2 | 7  | 12  |
    # |   2   | 2020-01-03       | 3 | 8  | 13  |
    # |   3   | 2020-01-04       | 4 | 9  | 14  |
    # |   4   | 2020-01-05       | 5 | 10 | 15  |
    expected = pd.DataFrame({
        "date": dates,
        "A": [1, 2, 3, 4, 5],
        "B": [6, 7, 8, 9, 10],
        "C": [11, 12, 13, 14, 15]
    })

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

def test_partial_overlap():
    # Test Case: Partial Overlap
    # Purpose:
    # Verify that the function correctly identifies the longest common date range
    # when DataFrames have partially overlapping dates.

    # Create dates for df1 and df2
    dates1 = pd.date_range(start="2020-01-01", periods=5, freq="D")
    dates2 = pd.date_range(start="2020-01-03", periods=5, freq="D")

    # Create DataFrame df1
    # Input df1:
    # | Index |       date       | A |
    # |-------|------------------|---|
    # |   0   | 2020-01-01       | 1 |
    # |   1   | 2020-01-02       | 2 |
    # |   2   | 2020-01-03       | 3 |
    # |   3   | 2020-01-04       | 4 |
    # |   4   | 2020-01-05       | 5 |
    df1 = pd.DataFrame({"date": dates1, "A": [1, 2, 3, 4, 5]})

    # Create DataFrame df2
    # Input df2:
    # | Index |       date       | B |
    # |-------|------------------|---|
    # |   0   | 2020-01-03       | 6 |
    # |   1   | 2020-01-04       | 7 |
    # |   2   | 2020-01-05       | 8 |
    # |   3   | 2020-01-06       | 9 |
    # |   4   | 2020-01-07       |10 |
    df2 = pd.DataFrame({"date": dates2, "B": [6, 7, 8, 9, 10]})

    # Call the function with the DataFrames
    result = get_longest_common_date_range([df1, df2])

    # Expected result is dates from 2020-01-03 to 2020-01-05
    # Expected Output:
    # | Index |       date       | A | B |
    # |-------|------------------|---|---|
    # |   0   | 2020-01-03       | 3 | 6 |
    # |   1   | 2020-01-04       | 4 | 7 |
    # |   2   | 2020-01-05       | 5 | 8 |
    expected_dates = pd.date_range(start="2020-01-03", end="2020-01-05", freq="D")
    expected = pd.DataFrame({
        "date": expected_dates,
        "A": [3, 4, 5],
        "B": [6, 7, 8]
    })

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

def test_no_overlap():
    # Test Case: No Overlap
    # Purpose:
    # Verify that the function returns None when there is no overlapping date range between the DataFrames.

    # Create dates for df1 and df2 with no overlap
    dates1 = pd.date_range(start="2020-01-01", periods=5, freq="D")
    dates2 = pd.date_range(start="2020-02-01", periods=5, freq="D")

    # Create DataFrame df1
    # Input df1:
    # | Index |       date       | A |
    # |-------|------------------|---|
    # |   0   | 2020-01-01       | 1 |
    # |   1   | 2020-01-02       | 2 |
    # |   2   | 2020-01-03       | 3 |
    # |   3   | 2020-01-04       | 4 |
    # |   4   | 2020-01-05       | 5 |
    df1 = pd.DataFrame({"date": dates1, "A": [1, 2, 3, 4, 5]})

    # Create DataFrame df2
    # Input df2:
    # | Index |       date       | B |
    # |-------|------------------|---|
    # |   0   | 2020-02-01       | 6 |
    # |   1   | 2020-02-02       | 7 |
    # |   2   | 2020-02-03       | 8 |
    # |   3   | 2020-02-04       | 9 |
    # |   4   | 2020-02-05       |10 |
    df2 = pd.DataFrame({"date": dates2, "B": [6, 7, 8, 9, 10]})

    # Call the function with the DataFrames
    result = get_longest_common_date_range([df1, df2])

    # Expected Output: None
    assert result is None, "Expected result to be None when there is no overlapping date range."

def test_missing_values():
    # Test Case: Missing Values
    # Purpose:
    # Verify that the function correctly identifies the longest contiguous date range when DataFrames have missing values.

    # Create sample dates
    dates = pd.date_range(start="2020-01-01", periods=5, freq="D")

    # Create DataFrame df1 with missing values
    # Input df1:
    # | Index |       date       |  A   |
    # |-------|------------------|------|
    # |   0   | 2020-01-01       | 1    |
    # |   1   | 2020-01-02       | None |
    # |   2   | 2020-01-03       | 3    |
    # |   3   | 2020-01-04       | None |
    # |   4   | 2020-01-05       | 5    |
    df1 = pd.DataFrame({"date": dates, "A": [1, None, 3, None, 5]})

    # Create DataFrame df2 with missing values
    # Input df2:
    # | Index |       date       |  B   |
    # |-------|------------------|------|
    # |   0   | 2020-01-01       | 6    |
    # |   1   | 2020-01-02       | 7    |
    # |   2   | 2020-01-03       | None |
    # |   3   | 2020-01-04       | 9    |
    # |   4   | 2020-01-05       | 10   |
    df2 = pd.DataFrame({"date": dates, "B": [6, 7, None, 9, 10]})

    # Call the function with the DataFrames
    result = get_longest_common_date_range([df1, df2])

    # Expected Output:
    # | Index |       date       | A |  B  |
    # |-------|------------------|---|-----|
    # |   0   | 2020-01-05       | 5 | 10  |
    expected_dates = pd.to_datetime(["2020-01-05"])
    expected = pd.DataFrame({
        "date": expected_dates,
        "A": [5],
        "B": [10]
    })

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

def test_single_dataframe():
    # Test Case: Single DataFrame
    # Purpose:
    # Verify that the function works correctly when only a single DataFrame is provided.

    # Create sample dates
    dates = pd.date_range(start="2020-01-01", periods=3, freq="D")

    # Create a single DataFrame df
    # Input df:
    # | Index |       date       | A |
    # |-------|------------------|---|
    # |   0   | 2020-01-01       | 1 |
    # |   1   | 2020-01-02       | 2 |
    # |   2   | 2020-01-03       | 3 |
    df = pd.DataFrame({"date": dates, "A": [1, 2, 3]})

    # Call the function with the single DataFrame
    result = get_longest_common_date_range([df])

    # Expected Output:
    # | Index |       date       | A |
    # |-------|------------------|---|
    # |   0   | 2020-01-01       | 1 |
    # |   1   | 2020-01-02       | 2 |
    # |   2   | 2020-01-03       | 3 |
    expected = df.copy()

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

def test_non_contiguous_blocks():
    # Test Case: Non-Contiguous Blocks
    # Purpose:
    # Verify that the function correctly identifies the longest contiguous block when DataFrames have multiple non-contiguous blocks due to missing values.

    # Create sample dates
    dates = pd.date_range(start="2020-01-01", periods=10, freq="D")

    # Create DataFrame df1 with missing values
    # Input df1:
    # | Index |       date       |  A   |
    # |-------|------------------|------|
    # |   0   | 2020-01-01       | 0    |
    # |   1   | 2020-01-02       | 1    |
    # |   2   | 2020-01-03       | 2    |
    # |   3   | 2020-01-04       | None |
    # |   4   | 2020-01-05       | 4    |
    # |   5   | 2020-01-06       | 5    |
    # |   6   | 2020-01-07       | 6    |
    # |   7   | 2020-01-08       | None |
    # |   8   | 2020-01-09       | 8    |
    # |   9   | 2020-01-10       | 9    |
    df1 = pd.DataFrame({"date": dates, "A": range(10)})
    df1.loc[3, "A"] = None  # Introduce NaN at index 3
    df1.loc[7, "A"] = None  # Introduce NaN at index 7

    # Create DataFrame df2 with missing values
    # Input df2:
    # | Index |       date       |   B   |
    # |-------|------------------|-------|
    # |   0   | 2020-01-01       | 10    |
    # |   1   | 2020-01-02       | 11    |
    # |   2   | 2020-01-03       | 12    |
    # |   3   | 2020-01-04       | 13    |
    # |   4   | 2020-01-05       | 14    |
    # |   5   | 2020-01-06       | None  |
    # |   6   | 2020-01-07       | 16    |
    # |   7   | 2020-01-08       | None  |
    # |   8   | 2020-01-09       | 18    |
    # |   9   | 2020-01-10       | 19    |
    df2 = pd.DataFrame({"date": dates, "B": range(10, 20)})
    df2.loc[5, "B"] = None  # Introduce NaN at index 5
    df2.loc[7, "B"] = None  # Introduce NaN at index 7

    # Call the function with the DataFrames
    result = get_longest_common_date_range([df1, df2])

    # Expected Output:
    # | Index |       date       | A |  B  |
    # |-------|------------------|---|-----|
    # |   0   | 2020-01-01       | 0 | 10  |
    # |   1   | 2020-01-02       | 1 | 11  |
    # |   2   | 2020-01-03       | 2 | 12  |
    expected_dates = pd.to_datetime(["2020-01-01", "2020-01-02", "2020-01-03"])
    expected = pd.DataFrame({
        "date": expected_dates,
        "A": [0, 1, 2],
        "B": [10, 11, 12]
    })

    # Assert that the result matches the expected DataFrame
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
