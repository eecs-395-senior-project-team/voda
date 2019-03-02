"""
Tests for the details endpoint.
"""
import requests


"""
Helper functions.
"""
def request_details_with_source():
    """
    call for the detail endpoint with a source value used by the detail tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/details?source=7')

def request_details_no_source():
    """
    call for the detail with no source value endpoint used by the source tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/details')

"""
Tests.
"""
def test_details_status_code_with_soure():
    """
    test that the status_code of the detail http response is 200 when it has a source value
    """
    assert request_details_with_source().status_code == 200

def test_details_content_with_source():
    """
    test that the detail http response body returns the proper message when it has a source value
    """
    assert request_details_with_source().content == b'Returns the full details for water supply 7.'

def test_details_details_code_no_soure():
    """
    test that the status_code of the detail http response is 200 when it has a source value
    """
    assert request_details_no_source().status_code == 400
