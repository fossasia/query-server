"""
# We need to support absolute_import project-wide before this will work...

from .scrapers import scrapers, small_test


def test_small_test():
    small_test()
"""

import os
import sys

import pytest
import requests

PYTHON3 = sys.version_info.major >= 3
REASON = 'Python 3 blocked until #297 goes live'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


def test_true():
    assert True, "We have a problem!"


@pytest.mark.xfail(PYTHON3 or not TRAVIS_CI, reason=REASON)
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    assert response.status_code == 404


def make_engine_api_call(engine_name):
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    assert requests.get(url).status_code == 400, engine_name

    if engine_name in ('dailymotion', 'exalead', 'mojeek', 'yandex'):
        return  # These engines need to be fixed so that they pass this test
    response = requests.get(url + '?query=fossaisa&num=3')
    assert response.status_code == 200, '{}: {}'.format(engine_name,
                                                        response.status_code)
    links = response.json()
    # These engines run in search_without_count() mode so we do not test length
    if engine_name not in ('quora', 'youtube'):
        assert len(links) == 3, '{}: {}'.format(engine_name, len(links))
    assert all('link' in link for link in links), engine_name
    assert all('title' in link for link in links), engine_name


@pytest.mark.xfail(PYTHON3 or not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    engines = """ask baidu bing dailymotion duckduckgo exalead google
                 mojeek parsijoo quora yahoo yandex youtube""".split()
    for engine_name in (engine_names or engines):
        make_engine_api_call(engine_name)
