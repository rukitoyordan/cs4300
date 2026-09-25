import os
# https://docs.python.org/3/library/os.html
# https://www.geeksforgeeks.org/python/python-get-number-of-characters-words-spaces-and-lines-in-a-file/

def word_counter(file_name):
    '''Reads desired file_name and returns the number of whitespace separated words in it.'''
    word_count = 0
    # Check if the file exists properly or not.
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"File not found: {file_name}")

    with open(file_name, "r", encoding="utf-8") as count_file:
        for line in count_file:
            words = line.split()
            word_count += len(words)

    return word_count

