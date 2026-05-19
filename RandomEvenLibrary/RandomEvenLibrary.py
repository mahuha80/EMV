"""
RandomEvenLibrary - Generates random even numbers from 1 to 20

This library provides keywords for Robot Framework to work with random even numbers.
"""

import random
from robot.api.deco import keyword, library
from robot.api import logger


@library(scope='GLOBAL', doc_format='ROBOT')
class RandomEvenLibrary:
    """
    RandomEvenLibrary - Robot Framework library for even numbers

    This library generates random even numbers from 1 to 20.

    == Importing ==

    When using this library you need to use one of the following import statements:

    | Library | RandomEvenLibrary |

    == Example ==

    | *** Test Cases ***
    | My Test
    |     ${even}=    Get Random Even Number
    |     Log    Got even number: ${even}
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.0'

    def __init__(self):
        """Initialize RandomEvenLibrary"""
        self.even_numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        self._last_number = None

    @keyword
    def get_random_even_number(self):
        """
        Returns a random even number between 1 and 20.

        The returned numbers are: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20

        Returns a random selection from these values each time.

        == Example ==

        | ${even}=    Get Random Even Number
        | Log    ${even}
        """
        self._last_number = random.choice(self.even_numbers)
        logger.info(f"Generated random even number: {self._last_number}")
        return self._last_number

    @keyword
    def get_random_even_numbers(self, count=5):
        """
        Returns a list of random even numbers between 1 and 20.

        The `count` argument specifies how many random even numbers to generate.
        The default value is 5.

        == Arguments ==
        | Argument | Default | Description |
        | count | 5 | Number of even numbers to generate |

        == Example ==

        | ${evens}=    Get Random Even Numbers
        | Log List    ${evens}
        | ${three_evens}=    Get Random Even Numbers    3
        """
        count = int(count)
        result = [random.choice(self.even_numbers) for _ in range(count)]
        logger.info(f"Generated {count} random even numbers: {result}")
        return result

    @keyword
    def get_all_even_numbers(self):
        """
        Returns all even numbers from 1 to 20.

        This keyword returns the complete list of valid even numbers
        without randomization.

        Returns: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

        == Example ==

        | ${all_evens}=    Get All Even Numbers
        | Log List    ${all_evens}
        | Should Contain    ${all_evens}    2
        """
        logger.info(f"All even numbers: {self.even_numbers}")
        return self.even_numbers

    @keyword
    def is_even_number_valid(self, number):
        """
        Validates if a number is a valid even number in range 1-20.

        == Arguments ==
        | Argument | Description |
        | number | The number to validate |

        Returns `True` if the number is a valid even number (2, 4, 6, 8, 10, 12, 14, 16, 18, 20),
        otherwise returns `False`.

        == Example ==

        | ${valid}=    Is Even Number Valid    4
        | Should Be True    ${valid}
        | ${invalid}=    Is Even Number Valid    5
        | Should Not Be True    ${invalid}
        """
        try:
            num = int(number)
            result = num in self.even_numbers
            logger.info(f"Validating {number}: {result}")
            return result
        except (ValueError, TypeError):
            logger.warn(f"Invalid input: {number} is not a number")
            return False

    @keyword
    def get_last_generated_number(self):
        """
        Returns the last generated random even number.

        If no number has been generated yet, returns None.

        == Example ==

        | Get Random Even Number
        | ${last}=    Get Last Generated Number
        | Log    Last number was: ${last}
        """
        logger.info(f"Last generated number: {self._last_number}")
        return self._last_number

