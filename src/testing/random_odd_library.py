"""
Random Odd Numbers Library
Provides keywords for generating random odd numbers from 1 to 20
"""

import random
from robot.api.deco import keyword


class RandomOddLibrary:
    """Robot Framework library for random odd numbers"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """Initialize the library"""
        self.odd_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    @keyword
    def get_random_odd_number(self):
        """
        Returns a random odd number between 1 and 20

        Example:
            ${odd_num}=    Get Random Odd Number
            Log    ${odd_num}
        """
        return random.choice(self.odd_numbers)

    @keyword
    def get_random_odd_numbers(self, count=5):
        """
        Returns a list of random odd numbers between 1 and 20

        Args:
            count: Number of odd numbers to generate (default: 5)

        Example:
            ${odd_list}=    Get Random Odd Numbers    3
            Log List    ${odd_list}
        """
        return [random.choice(self.odd_numbers) for _ in range(int(count))]

    @keyword
    def get_all_odd_numbers(self):
        """
        Returns all odd numbers from 1 to 20

        Example:
            ${all_odd}=    Get All Odd Numbers
            Log List    ${all_odd}
        """
        return self.odd_numbers

    @keyword
    def is_odd_number_valid(self, number):
        """
        Checks if a number is a valid odd number in range 1-20

        Args:
            number: The number to check

        Returns:
            True if number is odd and in range, False otherwise

        Example:
            ${is_valid}=    Is Odd Number Valid    5
        """
        try:
            num = int(number)
            return num in self.odd_numbers
        except (ValueError, TypeError):
            return False

