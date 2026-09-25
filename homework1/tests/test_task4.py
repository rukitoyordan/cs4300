import pytest
# src to be able to run globally from homework1/
from src import task4


## Duck Typing
# https://realpython.com/duck-typing-python/
# Tests: Final Pricing after Discount
@pytest.mark.parametrize("price, discount, expected", [
    # Some edge cases were discovered/learned about by using AI.
    (100, 20, 80),(100, 100, 0),(200, 12.5, 175.0),(80.0, 12.5, 70.0),(1, 15, 0.85),(3.899, 10, pytest.approx(3.5091)),(0.0, 50, 0.0)
])
def test_calculate_discount(price, discount, expected):
    assert task4.calculate_discount(price, discount) == expected

@pytest.mark.parametrize("price, discount", [
    ("fifty dollars", 25),(49.99, "ten percent"),(None, 75),("100", 20.5),(100, "20")
])
def test_calculate_discount_numbers_only_check(price, discount):
    with pytest.raises(TypeError):
        task4.calculate_discount(price, discount)

@pytest.mark.parametrize("price, discount", [
    (-1, 25),(65, -4),(100, 101),(-30, 25)
])
def test_calculate_discount_range_acceptable(price, discount):
    with pytest.raises(ValueError):
        task4.calculate_discount(price, discount)