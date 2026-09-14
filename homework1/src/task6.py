import os
# https://docs.python.org/3/library/os.html
# https://www.geeksforgeeks.org/python/python-get-number-of-characters-words-spaces-and-lines-in-a-file/

file = "task6_read_me.txt"

def word_counter(file):
    '''Reads task6_read_me.txt and counts the number of words in it.'''
    words = 0
    # Check if the file exists properly or not.
    if os.path.exists(file) == False:
        return 0

    with open(file, "r") as count_file:
        for x in count_file:
            word = x.split()
            words += len(word)

    return words

