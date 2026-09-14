import pytest
# src to be able to run globally from homework1/
from src import task7
import requests


# Tests: Requests Link Validation
def test_request_website_status_valid():
    '''Tests for a valid website address.'''
    url = task7.request_website_status("https://www.youtube.com/")
    assert type(url) is bool
    assert url == True

def test_request_website_status_invalid():
    '''Tests for a native 404 Error Code.'''
    url = task7.request_website_status("https://www.youtube.com/not-working")
    assert type(url) is bool
    assert url == False