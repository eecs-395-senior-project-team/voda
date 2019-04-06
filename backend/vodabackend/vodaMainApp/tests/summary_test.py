"""
Tests for summary endpoint.
"""
from vodabackend.vodaMainApp.views import summary
import pytest


requestWithSource = '/summary?source=7'
requestNoSource = '/summary'

###############################################################################
# Tests.
###############################################################################
def test_summary_status_code_with_soure(rf):
    """
    test that the status_code of the summary http response is 200 when it has a source value
    """
    request = rf.get(requestWithSource)
    response = summary(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_summary_content(rf):
    """
    test that the summary http response body returns the proper message when it has a source value
    """
    request = rf.get(requestWithSource)
    response = summary(request)
    assert response.content == b'Returns the summary details for water supply 7.'


def test_summary_status_code_no_soure(rf):
    """
    test that the status_code of the summary http response is 400 if there's no source value
    """
    request = rf.get(requestNoSource)
    response = summary(request)
    assert response.status_code == 400
