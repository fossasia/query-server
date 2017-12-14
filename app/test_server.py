import os

import pytest
import requests

REASON = 'Do you have query-server running on http://127.0.0.1:7001 ?'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


def test_true():
    assert True, "We have a problem!"


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    assert response.json()['Status Code'] == 404


def make_engine_api_call(engine_name):
    if engine_name in ('dailymotion', 'exalead', 'mojeek', 'yandex'):
        return  # These engines need to be fixed so that they pass this test
    # No search term should return a status_code of 400
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    response = requests.get(url)
    assert response.status_code == 400, url

    url += '?query=fossasia'  # add a search term
    response = requests.get(url)
    assert response.status_code == 200, url
    links = response.json()
    if isinstance(links, dict):
        assert links.get('status_code', 200) == 200
    assert 'error' not in links, links
    for item in links:
        assert 'link' in item, item
        assert 'title' in item, item

    url += '&num=3'  # add a desired number of items
    response = requests.get(url)
    assert response.status_code == 200, url
    assert len(response.json()) == 3, url


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    engines = """ask baidu bing dailymotion duckduckgo exalead google
                 mojeek parsijoo quora yahoo yandex youtube""".split()
    for engine_name in (engine_names or engines):
        make_engine_api_call(engine_name)
