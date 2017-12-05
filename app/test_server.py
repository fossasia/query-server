"""
# Let's get pytest turned on before we start testing in earnest

from .scrapers import small_test


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
    assert response.json()['Status Code'] == 404


def make_engine_api_call(engine_name):
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    assert requests.get(url).json()['Status Code'] == 400, engine_name


@pytest.mark.xfail(PYTHON3 or not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    engines = ['ask', 'ubaidu', 'bing', 'duckduckgo', 'tyoutube',
               'exalead', 'mojeek', 'google', 'quora', 'yahoo',
               'nyandex', 'parsijoo']
    for engine_name in (engine_names or engines):
        make_engine_api_call(engine_name)
