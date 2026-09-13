import pytest
# src to be able to run globally from homework1/
from src import task1


def test_hello_world(capsys):
    task1.hello_world()
    captured = capsys.readouterr()
    # Python adds \n after prints which is why the assert condition requires it to pass the test.
    assert captured.out == "Hello, World!\n"

# https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html

