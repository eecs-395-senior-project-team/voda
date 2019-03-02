"""
Tests for root endpoint.
"""
from vodabackend.vodaMainApp.views import root


def test_root(rf):
    """ Tests root endpoint

    Checks that the response is the phrase 'Server Alive.'

    Args:
        rf: Pytest-django Fixture for mocking incoming requests.
            https://pytest-django.readthedocs.io/en/latest/helpers.html#rf-requestfactory
    """
    request = rf.get('/')
    response = root(request)
    assert response.content == b"Server Alive."
