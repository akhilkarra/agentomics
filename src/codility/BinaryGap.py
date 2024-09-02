# By Akhil Karra.
# The following code is my solution to the BinaryGap Problem from Module 1 in
# Codility Developer Training. This solution was my 2nd attempt, was drafted in 59 minutes and
# earned a score of 100%. Changes were made manually and automatically only to improve style.
# Link to test report: https://app.codility.com/demo/results/trainingKNGRQ2-F2B/


def solution(n: int) -> int:
    """Returns the longest binary gap in a positive integer N.

    Args:
        n: positive integer such that 1 &lt;<= N &lt;<= 2,147,483,647

    Returns:
        positive integer that represents the binary gap within N
    """
    # Confirm the condition that 1 <= N <= 2,147,483,647 is met
    assert 1 <= n <= 2147483647

    largest_gap = 0  # Variable to store the current largest gap between 1s seen so far
    current_gap = 0  # Variable keeping track of the current gap between 1s
    in_gap = (
        False  # Variable keeping track of whether we are currently looking at a gap
    )

    # Iterate through the entire binary representation of N
    while n > 0:
        if not in_gap:  # If we are currently not in a gap
            if n % 2 == 1:  # but the current right-most bit is 1,
                in_gap = True  # we are now looking for a gap.
                n = n // 2  # Go to the next bit.

            else:  # Otherwise,
                n = n // 2  # Do nothing and go to the next bit

        else:  # If we are currently in a gap
            if n % 2 == 0:  # and the current right-most bit it 0,
                current_gap += 1  # we have a 0 in the current gap.
                n = n // 2  # Go to the next bit.

            else:  # But if the right-most digit is a 1, we have finished a gap.
                if current_gap > largest_gap:
                    largest_gap = (
                        current_gap  # Update the largest gap found accordingly
                    )
                current_gap = 0  # We are now looking for a new gap
                n = n // 2  # Go to the next bit

    return largest_gap  # The largest gap found by the end of the loop is the binary gap
