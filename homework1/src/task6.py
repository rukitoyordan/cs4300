import os
# https://docs.python.org/3/library/os.html
# https://www.geeksforgeeks.org/python/python-get-number-of-characters-words-spaces-and-lines-in-a-file/

file_name = "task6_read_me.txt"

def word_counter(file_name):
    '''Reads task6_read_me.txt and counts the number of words in it.'''
    word_count = 0
    # Check if the file exists properly or not.
    if not os.path.exists(file_name):
        return 0

    with open(file_name, "r", encoding="utf-8") as count_file:
        for line in count_file:
            word = line.split()
            word_count += len(word)

    return word_count

