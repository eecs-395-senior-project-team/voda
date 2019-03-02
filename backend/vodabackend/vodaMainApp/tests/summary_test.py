"""
Tests for summary endpoint.
"""
import requests


"""
Helper functions.
"""
def request_summary_with_source():
    """
    call for the summary endpoint with a source value used by the source tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/summary?source=7')

def request_summary_no_source():
    """
    call for the summary with no source value endpoint used by the source tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/summary')

"""
Tests.
"""
def test_summary_status_code_with_soure():
    """
    test that the status_code of the summary http response is 200 when it has a source value
    """
    assert request_summary_with_source().status_code == 200

def test_summary_content():
    """
    test that the summary http response body returns the proper message when it has a source value
    """
    assert request_summary_with_source().content == b'Returns the summary details for water supply 7.'

def test_summary_status_code_no_soure():
    """
    test that the status_code of the summary http response is 400 if there's no source value
    """
    assert request_summary_no_source().status_code == 400
