import pytest
from codility.BinaryGap import solution


@pytest.mark.parametrize(
    "n, expected",
    {
        (9, 2),
        (529, 4),
        (1041, 5),
        (1, 0),
        (5, 1),
        (2147483647, 0),
        (6, 0),
        (328, 2),
        (16, 0),
        (1024, 0),
        (9, 2),
        (11, 1),
        (19, 2),
        (42, 1),
        (1162, 3),
        (51712, 2),
        (20, 1),
        (561892, 3),
        (66561, 9),
        (74901729, 4),
        (805306373, 25),
        (1376796946, 5),
        (1073741825, 29),
        (1610612737, 28),
    },
)
def test_solution(n: int, expected: int) -> None:
    assert solution(n) == expected
