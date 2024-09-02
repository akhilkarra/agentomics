# By Akhil Karra.
# The following code is my solution to the OddOccurrences Problem from Module 2 in
# Codility Developer Training.
import typing


def solution(a: typing.List[int]) -> int:
    """For a non-empty array A of integers such that all but one number is
    repeated twice, this function returns the value of the number that is not
    repeated.

    Args:
        a: a non-empty array consisting of an odd number N of integers

    Returns:
        an integer showing the value of the integer not repeated in A
    """
    # Remove the duplicates in the list
    for element in a:
        a.remove(element)
        if element in a:
            a.remove(element)

    # Return the only element left in the list
    return a[0]
