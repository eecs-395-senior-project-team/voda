"""
Tests for debug endpoint.
"""
from vodabackend.vodaMainApp.views import debug


def test_debug(rf):
    """ Tests debug endpoint

    Checks that the response is valid with the expected details.

    Args:
        rf: Pytest-django Fixture for mocking incoming requests.
            https://pytest-django.readthedocs.io/en/latest/helpers.html#rf-requestfactory
    """
    request = rf.get('/debug')
    response = debug(request)
    expected_response = (b'Request received: host: testserver, type: GET,',
                         b'GET params: <QueryDict: {}>, POST params: <QueryDict: {}>')
    assert response.content == expected_response
