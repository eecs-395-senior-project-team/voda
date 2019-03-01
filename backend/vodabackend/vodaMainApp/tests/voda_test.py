from django.test import TestCase

# Create your tests here.


import requests

"""
call for the map endpoint used by the map tests
"""
def request_map():
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/map')

"""
test that the status_code of the map http response is 200
"""
def test_map_status_code():
	assert request_map().status_code == 200

"""
test that the map http response body returns the proper message
"""
def test_map_content():
	assert request_map().content == b'Returns a list of water supplies and a 1-10 value with the quality of the water.'


"""
call for the summary endpoint with a source value used by the source tests
"""
def request_summary_with_source():
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/summary?source=7')

"""
test that the status_code of the summary http response is 200 when it has a source value
"""
def test_summary_status_code_with_soure():
	assert request_summary_with_source().status_code == 200

"""
test that the summary http response body returns the proper message when it has a source value
"""
def test_map_content():
	assert request_summary_with_source().content == b'Returns the summary details for water supply 7.'


"""
call for the summary with no source value endpoint used by the source tests
"""
def request_summary_no_source():
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/summary')

"""
test that the status_code of the summary http response is 400 if there's no source value
"""
def test_summary_status_code_no_soure():
	assert request_summary_no_source().status_code == 400


"""
call for the detail endpoint with a source value used by the detail tests
"""
def request_details_with_source():
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/details?source=7')

"""
test that the status_code of the detail http response is 200 when it has a source value
"""
def test_details_status_code_with_soure():
	assert request_details_with_source().status_code == 200

"""
test that the detail http response body returns the proper message when it has a source value
"""
def test_details_content_with_source():
	assert request_details_with_source().content == b'Returns the full details for water supply 7.'


"""
call for the detail with no source value endpoint used by the source tests
"""
def request_details_no_source():
    # Send a request to the API server and store the response.
    return requests.get('http://0.0.0.0:8000/details')

"""
test that the status_code of the detail http response is 200 when it has a source value
"""
def test_details_details_code_no_soure():
	assert request_details_no_source().status_code == 400
