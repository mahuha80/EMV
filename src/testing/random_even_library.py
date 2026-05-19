"""
Random Even Numbers Library
Provides keywords for generating random even numbers from 1 to 20
"""

import random
from robot.api.deco import keyword


class RandomEvenLibrary:
    """Robot Framework library for random even numbers"""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        """Initialize the library"""
        self.even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    @keyword
    def get_random_even_number(self):
        """
        Returns a random even number between 1 and 20

        Example:
            ${even_num}=    Get Random Even Number
            Log    ${even_num}
        """
        return random.choice(self.even_numbers)

    @keyword
    def get_random_even_numbers(self, count=5):
        """
        Returns a list of random even numbers between 1 and 20

        Args:
            count: Number of even numbers to generate (default: 5)

        Example:
            ${even_list}=    Get Random Even Numbers    3
            Log List    ${even_list}
        """
        return [random.choice(self.even_numbers) for _ in range(int(count))]

    @keyword
    def get_all_even_numbers(self):
        """
        Returns all even numbers from 1 to 20

        Example:
            ${all_even}=    Get All Even Numbers
            Log List    ${all_even}
        """
        return self.even_numbers

    @keyword
    def is_even_number_valid(self, number):
        """
        Checks if a number is a valid even number in range 1-20

        Args:
            number: The number to check

        Returns:
            True if number is even and in range, False otherwise

        Example:
            ${is_valid}=    Is Even Number Valid    4
        """
        try:
            num = int(number)
            return num in self.even_numbers
        except (ValueError, TypeError):
            return False

