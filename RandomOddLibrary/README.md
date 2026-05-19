# Random Odd Library

A Robot Framework library that generates random odd numbers from 1 to 20.

## Installation

```bash
cd RandomOddLibrary
pip install -e .
```

## Usage

```robot
*** Settings ***
Library    RandomOddLibrary

*** Test Cases ***
Test Odd Numbers
    ${odd}=    Get Random Odd Number
    Log    ${odd}
```

## Keywords

### Get Random Odd Number
Returns a random odd number between 1 and 20 (1, 3, 5, 7, 9, 11, 13, 15, 17, 19)

### Get Random Odd Numbers
Returns a list of random odd numbers

**Arguments:**
- count (optional): Number of odd numbers to generate (default: 5)

### Get All Odd Numbers
Returns all odd numbers from 1 to 20 as a list

### Is Odd Number Valid
Checks if a number is a valid odd number in range 1-20

**Arguments:**
- number: The number to validate

**Returns:** True or False

