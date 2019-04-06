import requests
from scrapy.http import TextResponse, Request
from vodaData.getContaminantsScraper import FindContaminants


###############################################################################
# Helper functions.
###############################################################################


def file_len(file_name):
    with open(file_name) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


def online_response_from_url (url=None):

    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    original_resp = requests.get(url)
    response = TextResponse(url=url, request=request, body=original_resp.text, encoding='utf-8')

    return response

###############################################################################
# Tests
###############################################################################


def test_get_contaminants_parse():
    url = "https://www.ewg.org/tapwater/chemical-contaminants.php"
    spider = FindContaminants()
    spider.parse(online_response_from_url(url=url))
    flen = file_len("./vodaData/AllContaminants.txt")
    assert flen == 200

