import pytest
# src to be able to run globally from homework1/
from src import task2


# Tests: Integer
@pytest.mark.parametrize("int1, int2, expected", [(8, 7, 56), (-6, -6, 36), (-4, 3, -12)])
def test_integer_mult(int1, int2, expected):
    assert task2.integer_mult(int1, int2) == expected

# Tests: Floating-Point Numbers
@pytest.mark.parametrize("float1, float2, expected", [(10.0, 5.0, 2.0), (29.7, -4.8, -6.1875), (7.0, 16.0, 0.4375)])
def test_float_division(float1, float2, expected):
    assert task2.float_division(float1, float2) == expected

# Tests: Strings
@pytest.mark.parametrize("strng, expected", [("friends", "sdneirf"), ("five hundred twenty", "ytnewt derdnuh evif"), (" ", " ")])
def test_string_invert(strng, expected):
    assert task2.string_invert(strng) == expected

# Test: Booleans
@pytest.mark.parametrize("strng, expected", [("HASTINGS", True), ("hastings", False), ("", False)])
def test_is_capitalized(strng, expected):
    assert task2.is_capitalized(strng) == expected

# https://docs.pytest.org/en/stable/how-to/parametrize.html