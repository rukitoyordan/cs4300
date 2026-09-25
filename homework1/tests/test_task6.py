import pytest
# src to be able to run globally from homework1/
from src import task6
from pathlib import Path

TASK6_FILE = Path(__file__).resolve().parents[1] / "task6_read_me.txt"

# Tests: Word Counter on the task6_read_me.txt file
def test_task6_read_me_word_counter():
    assert task6.word_counter(TASK6_FILE) == 127

# Tests: Word Counter on File
@pytest.mark.parametrize("file_contents, expected_count", [
    ("one two three", 3),
    ("one\n two   three\n", 3),
    ("", 0),
])

def test_word_counter(file_contents, expected_count, tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text(file_contents, encoding="utf-8")

    assert task6.word_counter(test_file) == expected_count

# Test: Missing file error
def test_word_counter_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        task6.word_counter(missing_file)
