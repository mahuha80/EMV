"""
RandomOddLibrary - Generates random odd numbers from 1 to 20

This library provides keywords for Robot Framework to work with random odd numbers.
"""

import random
from robot.api.deco import keyword, library
from robot.api import logger


@library(scope='GLOBAL', doc_format='ROBOT')
class RandomOddLibrary:
    """
    RandomOddLibrary - Robot Framework library for odd numbers

    This library generates random odd numbers from 1 to 20.

    == Importing ==

    When using this library you need to use one of the following import statements:

    | Library | RandomOddLibrary |

    == Example ==

    | *** Test Cases ***
    | My Test
    |     ${odd}=    Get Random Odd Number
    |     Log    Got odd number: ${odd}
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    def __init__(self):
        """Initialize RandomOddLibrary"""
        self.odd_numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        self._last_number = None

    @keyword
    def get_random_odd_number(self):
        """
        Returns a random odd number between 1 and 20.

        The returned numbers are: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19

        Returns a random selection from these values each time.

        == Example ==

        | ${odd}=    Get Random Odd Number
        | Log    ${odd}
        """
        self._last_number = random.choice(self.odd_numbers)
        logger.info(f"Generated random odd number: {self._last_number}")
        return self._last_number

    @keyword
    def get_random_odd_numbers(self, count=5):
        """
        Returns a list of random odd numbers between 1 and 20.

        The `count` argument specifies how many random odd numbers to generate.
        The default value is 5.

        == Arguments ==
        | Argument | Default | Description |
        | count | 5 | Number of odd numbers to generate |

        == Example ==

        | ${odds}=    Get Random Odd Numbers
        | Log List    ${odds}
        | ${three_odds}=    Get Random Odd Numbers    3
        """
        count = int(count)
        result = [random.choice(self.odd_numbers) for _ in range(count)]
        logger.info(f"Generated {count} random odd numbers: {result}")
        return result

    @keyword
    def get_all_odd_numbers(self):
        """
        Returns all odd numbers from 1 to 20.

        This keyword returns the complete list of valid odd numbers
        without randomization.

        Returns: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

        == Example ==

        | ${all_odds}=    Get All Odd Numbers
        | Log List    ${all_odds}
        | Should Contain    ${all_odds}    1
        """
        logger.info(f"All odd numbers: {self.odd_numbers}")
        return self.odd_numbers

    @keyword
    def is_odd_number_valid(self, number):
        """
        Validates if a number is a valid odd number in range 1-20.

        == Arguments ==
        | Argument | Description |
        | number | The number to validate |

        Returns `True` if the number is a valid odd number (1, 3, 5, 7, 9, 11, 13, 15, 17, 19),
        otherwise returns `False`.

        == Example ==

        | ${valid}=    Is Odd Number Valid    5
        | Should Be True    ${valid}
        | ${invalid}=    Is Odd Number Valid    4
        | Should Not Be True    ${invalid}
        """
        try:
            num = int(number)
            result = num in self.odd_numbers
            logger.info(f"Validating {number}: {result}")
            return result
        except (ValueError, TypeError):
            logger.warn(f"Invalid input: {number} is not a number")
            return False

    @keyword
    def get_last_generated_number(self):
        """
        Returns the last generated random odd number.

        If no number has been generated yet, returns None.

        == Example ==

        | Get Random Odd Number
        | ${last}=    Get Last Generated Number
        | Log    Last number was: ${last}
        """
        logger.info(f"Last generated number: {self._last_number}")
        return self._last_number

