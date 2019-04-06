"""
Tests for the map endpoint.
"""
from vodabackend.vodaMainApp.views import map_endpoint
import pytest

# inputs for http requests
mapRequest = '/map'

###############################################################################
# Helper functions.
###############################################################################
def request_map():
    """
    call for the map endpoint used by the map tests
    """
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/map')


###############################################################################
# Tests.
###############################################################################
@pytest.mark.django_db
def test_map_status_code(rf):
    """
    test that the status_code of the map http response is 200
    """
    request = rf.get(mapRequest)
    response = map_endpoint(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_map_content(rf):
    """
    test that the map http response body returns the proper message
    """
    request = rf.get(mapRequest)
    response = map_endpoint(request)
    
    assert response.content == b'Returns a list of water supplies and a 1-10 value with the quality of the water.'
