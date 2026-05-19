*** Settings ***
Library        Collections
Library        ../src/testing/random_even_library.py
Library        ../src/testing/random_odd_library.py

*** Test Cases ***
Test Get Random Even Number
    [Documentation]    Demo: Get a single random even number
    ${even}=           Get Random Even Number
    Log                Random even number: ${even}
    ${is_valid}=       Is Even Number Valid    ${even}
    Should Be True     ${is_valid}

Test Get Random Odd Number
    [Documentation]    Demo: Get a single random odd number
    ${odd}=            Get Random Odd Number
    Log                Random odd number: ${odd}
    ${is_valid}=       Is Odd Number Valid    ${odd}
    Should Be True     ${is_valid}

Test Get Multiple Even Numbers
    [Documentation]    Demo: Get multiple random even numbers
    ${even_list}=      Get Random Even Numbers    5
    Log List           ${even_list}
    Length Should Be   ${even_list}    5

Test Get Multiple Odd Numbers
    [Documentation]    Demo: Get multiple random odd numbers
    ${odd_list}=       Get Random Odd Numbers    5
    Log List           ${odd_list}
    Length Should Be   ${odd_list}    5

Test Get All Even Numbers
    [Documentation]    Demo: Get all even numbers
    ${all_even}=       Get All Even Numbers
    Log List           ${all_even}
    Should Be Equal    ${all_even}    [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

Test Get All Odd Numbers
    [Documentation]    Demo: Get all odd numbers
    ${all_odd}=        Get All Odd Numbers
    Log List           ${all_odd}
    Should Be Equal    ${all_odd}    [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

Test Validate Even Numbers
    [Documentation]    Demo: Validate even numbers
    ${valid}=          Is Even Number Valid    4
    Should Be True     ${valid}
    ${invalid}=        Is Even Number Valid    5
    Should Not Be True    ${invalid}

Test Validate Odd Numbers
    [Documentation]    Demo: Validate odd numbers
    ${valid}=          Is Odd Number Valid    5
    Should Be True     ${valid}
    ${invalid}=        Is Odd Number Valid    4
    Should Not Be True    ${invalid}

