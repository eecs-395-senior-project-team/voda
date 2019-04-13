"""
Tests for the map endpoint.
"""

from django.core.management import call_command
from django.test import TestCase
from vodabackend.vodaMainApp.views import map_endpoint
from vodabackend.vodaMainApp.models import State, Sources, Contaminants, SourceLevels, StateAvgLevels
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


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    
    with django_db_blocker.unblock():
        call_command('loaddata', 'testSources.json')



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
