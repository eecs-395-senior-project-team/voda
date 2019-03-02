"""
Tests for the map endpoint.
"""
import requests


"""
Helper functions.
"""
def request_map():
    """
    call for the map endpoint used by the map tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/map')

"""
Tests.
"""
def test_map_status_code():
    """
    test that the status_code of the map http response is 200
    """
    assert request_map().status_code == 200

def test_map_content():
    """
    test that the map http response body returns the proper message
    """
    assert request_map().content == b'Returns a list of water supplies and a 1-10 value with the quality of the water.'
