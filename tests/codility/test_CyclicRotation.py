import typing

import pytest

from codility.CyclicRotation import solution


@pytest.mark.parametrize(
    "a, k, expected",
    [
        ([3, 8, 9, 7, 6], 3, [9, 7, 6, 3, 8]),
        ([0, 0, 0], 1, [0, 0, 0]),
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        ([], 5, []),
        ([2], 17, [2]),
        ([2, 3], 13, [3, 2]),
        ([2, 3], 12, [2, 3]),
    ],
)
def test_solution(a: typing.List[int], k: int, expected: typing.List[int]) -> None:
    assert solution(a, k) == expected
