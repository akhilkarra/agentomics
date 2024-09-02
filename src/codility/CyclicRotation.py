# By Akhil Karra.
# The following code is my solution to the CyclicRotation Problem from Module 2 in
# Codility Developer Training. This solution was my 1st attempt, was drafted in 24 minutes and
# earned a score of 100%. Changes were made manually and automatically only to improve style.

import typing


def solution(a: typing.List[int], k: int) -> typing.List[int]:
    """Returns the given array rotated by K units.

    Args:
        a: an array of n integers such that 0 &lt;<= n &lt;<= 100 and given any element x,
        -1000 &lt;<= x &lt;<= 1000

        k: an integer such that 0 &lt;<= K &lt;<= 100

    Returns:
        an array of n integers rotated by K units
    """
    n = len(a)  # Let n be the the number of integers in A

    # Confirm that the constraints given in the problem statement are met
    assert (0 <= n <= 100 and 0 <= k <= 100 and -1000 <= x <= 1000 for x in a)

    # Define a new array with the same length as A, which will be the final array
    rotated_array = [0] * n

    # Iterate through the array A *in order*
    for index_of_a in range(n):
        new_index = (index_of_a + k) % n  # Use mod rules to get new index
        rotated_array[new_index] = a[index_of_a]  # Put element of A in new index

    return rotated_array  # Output the rotated array
