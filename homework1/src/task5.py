def list_favorite_books():
    '''Create a list of your favorite books, including book titles and authors.'''
    favorite_books = ["The Rise of Kyoshi by F.C. Yee", "Beautiful Creatures by Kami Garcia and Margaret Stohl", "The Four Agreements by Don Miguel Ruiz", "Origin by Dan Brown"]
    return favorite_books

def obtain_first_three_books(favorite_books):
    '''Apply list slicing to print the first three books in the favorite books list.'''
    first_three_books = favorite_books[:3]
    print(first_three_books)
    return first_three_books

def basic_student_database():
    '''Represents a basic student database, including student names and their corresponding student IDs.'''
    student_database = {"Edgar Feliciano": 802214567, "Ruth Shepard": 802229874, "Jason Laboy": 802193523, "John Stevenson": 802164211}
    return student_database
