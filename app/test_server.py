import os

import pytest
import requests

from .scrapers import small_test

REASON = 'Do you have query-server running on http://127.0.0.1:7001 ?'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


def test_true():
    assert True, "We have a problem!"


def test_small_test():
    small_test()


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    assert response.json()['Status Code'] == 404


def make_engine_api_call(engine_name):
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    assert requests.get(url).json()['Status Code'] == 400, engine_name


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    engines = """ask baidu bing dailymotion duckduckgo exalead google
                 mojeek parsijoo quora yahoo yandex youtube""".split()
    for engine_name in (engine_names or engines):
        make_engine_api_call(engine_name)
