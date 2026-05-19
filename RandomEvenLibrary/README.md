# Random Even Library

A Robot Framework library that generates random even numbers from 1 to 20.

## Installation

```bash
cd RandomEvenLibrary
pip install -e .
```

## Usage

```robot
*** Settings ***
Library    RandomEvenLibrary

*** Test Cases ***
Test Even Numbers
    ${even}=    Get Random Even Number
    Log    ${even}
```

## Keywords

### Get Random Even Number
Returns a random even number between 1 and 20 (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)

### Get Random Even Numbers
Returns a list of random even numbers

**Arguments:**
- count (optional): Number of even numbers to generate (default: 5)

### Get All Even Numbers
Returns all even numbers from 1 to 20 as a list

### Is Even Number Valid
Checks if a number is a valid even number in range 1-20

**Arguments:**
- number: The number to validate

**Returns:** True or False

