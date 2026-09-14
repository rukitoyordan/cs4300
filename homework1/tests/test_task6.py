import pytest
# src to be able to run globally from homework1/
from src import task6
import os


# Tests: Word Counter on File
@pytest.mark.parametrize("test_file, expected_count", [
    ("task6_read_me.txt", 127),  
    ("", 0)  
])
def test_word_counter(test_file, expected_count):
    assert task6.word_counter(test_file) == expected_count
