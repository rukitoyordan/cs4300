import pytest
# src to be able to run globally from homework1/
from src import task4


## Duck Typing
# https://realpython.com/duck-typing-python/
# Tests: Final Pricing after Discount
@pytest.mark.parametrize("price, discount, expected", [
    # Some edge cases were discovered/learned about by using AI.
    (100, 20, 80),(100, 100, 0),(True, 15, 0.85),(3.899, 10, 3.5091),(0.0, 50, 0.0)
])
def test_calculate_discount(price, discount, expected):
    assert task4.calculate_discount(price, discount) == expected