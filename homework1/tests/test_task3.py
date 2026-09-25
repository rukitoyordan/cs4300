import pytest
# src to be able to run globally from homework1/
from src import task3

# Prime Checks
@pytest.mark.parametrize("number, expected", [
    (-7, False),
    (0, False),
    (1, False),
    (2, True),
    (4, False),
    (9, False),
    (25, False),
    (97, True),
])
def test_is_prime(number, expected):
    assert task3.is_prime(number) is expected
    
## Control Structures
# Tests: If Statement
@pytest.mark.parametrize("number, expected", [
    (2929, "this number is positive."),
    (-2929, "this number is negative."),
    (0, "this number is zero."),
    (0.0, "this number is zero."),
    (3.14159239029487, "this number is positive."),
    (-101.14325, "this number is negative.")
])
def test_check_number_status(number, expected):
    assert task3.check_number_status(number) == expected

# Tests: For Loop
@pytest.mark.parametrize("expected", [
    ([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
])
def test_first_ten_prime_numbers(expected):
    assert task3.first_ten_prime_numbers() == expected

# Tests: While Loop
def test_sum_all_one_to_hundred():
    result = task3.sum_all_one_to_hundred()
    assert result == 5050