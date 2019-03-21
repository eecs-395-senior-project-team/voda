"""
Tests for the details endpoint.
"""
from vodabackend.vodaMainApp.views import details

# inputs for http requests
requestWithSource = '/details?source=7'
requestNoSource = '/details'

###############################################################################
# Tests.
###############################################################################
def test_details_status_code_with_soure(rf):
    """
    test that the status_code of the detail http response is 200 when it has a source value
    """
    request = rf.get(requestWithSource)
    response = details(request)
    assert response.status_code == 200


def test_details_content_with_source(rf):
    """
    test that the detail http response body returns the proper message when it has a source value
    """
    request = rf.get(requestWithSource)
    response = details(request)
    assert response.content == b'Returns the full details for water supply 7.'


def test_details_details_code_no_soure(rf):
    """
    test that the status_code of the detail http response is 200 when it has a source value
    """
    request = rf.get(requestNoSource)
    response = details(request)
    assert response.status_code == 400
