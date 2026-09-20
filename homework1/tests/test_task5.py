import pytest
# src to be able to run globally from homework1/
from src import task5


# Tests: Favorite Books
def test_list_favorite_books():
    favorite_books = task5.list_favorite_books()
    assert type(favorite_books) is list
    assert len(favorite_books) == 4
    assert "The Four Agreements by Don Miguel Ruiz" in favorite_books
    assert "The Rise of Kyoshi by F.C. Yee" in favorite_books
    assert "Origin by Dan Brown" in favorite_books
    assert "Beautiful Creatures by Kami Garcia and Margaret Stohl" in favorite_books

def test_obtain_first_three_books():
    favorite_books = task5.list_favorite_books()
    first_three_books = task5.obtain_first_three_books(favorite_books)
    assert type(first_three_books) is list
    assert len(first_three_books) == 3
    # Check if the slicing works properly.
    assert first_three_books == favorite_books[:3] 
    # Ensures the fourth book is not within the three books.
    assert "Origin by Dan Brown" not in first_three_books

def test_basic_student_database():
    student_database = task5.basic_student_database()
    assert type(student_database) is dict
    assert len(student_database) == 4
    proposed_database = {"Edgar Feliciano": 802214567, 
        "Ruth Shepard": 802229874, 
        "Jason Laboy": 802193523, 
        "John Stevenson": 802164211}
    assert student_database == proposed_database