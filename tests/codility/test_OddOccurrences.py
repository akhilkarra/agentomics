import typing

import pytest
from codility.OddOccurrences import solution


@pytest.mark.parametrize(
    "a, expected",
    [([9, 3, 9, 3, 9, 7, 9], 7)],
)
def test_solution(a: typing.List[int], expected: int) -> None:
    assert solution(a) == expected
