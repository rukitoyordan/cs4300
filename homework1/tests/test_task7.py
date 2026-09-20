import pytest
# src to be able to run globally from homework1/
from src import task7
import requests
from unittest.mock import Mock, patch
# https://docs.python.org/3/library/unittest.mock.html


# Tests: Requests Link Validation
@patch("src.task7.requests.get") # fake test
def test_request_website_status_valid(mock_get):
    '''Tests for a valid website address. (HTTP 200)'''
    mock_get.return_value = Mock(status_code=200)
    url = task7.request_website_status("https://www.youtube.com/")
    assert type(url) is bool
    assert url == True

@patch("src.task7.requests.get") 
def test_request_website_status_invalid(mock_get):
    '''Tests for a native 404 Error Code.'''
    mock_get.return_value = Mock(status_code=404)
    url = task7.request_website_status("https://www.youtube.com/not-working")
    assert type(url) is bool
    assert url == False

@patch("src.task7.requests.get") 
def test_request_website_status_network_error(mock_get):
    '''Tests for a network error.'''
    mock_get.side_effect = requests.RequestException("Network unavailable")
    url = task7.request_website_status("https://www.youtube.com/")
    assert type(url) is bool
    assert url == False