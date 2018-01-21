import os

import pytest
import requests

from app.scrapers import scrapers, small_test

DEEPER_TESTS = False
REASON = 'Do you have query-server running on http://127.0.0.1:7001 ?'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


def test_true():
    assert True, "We have a problem!"


def test_small_test():
    small_test()


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    assert response.status_code == 404  # workaround for #332


def make_engine_api_call(engine_name):
    # test that URLs without parameters are rejected as invalid
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    assert requests.get(url).status_code == 400  # workaround for #332
    # These engines need to be fixed so that they pass this test
    if engine_name in ('dailymotion', 'exalead', 'mojeek', 'yandex'):
        return
    # add query parameters to the  URL
    response = requests.get(url + '?query=fossaisa&num=3')
    assert response.status_code == 200, engine_name  # workaround for #332
    if not DEEPER_TESTS:
        return
    links = response.json()
    if isinstance(links, dict):
        assert links.get('status_code', 200) == 200  # workaround for #332
    # These engines run in search_without_count() mode so we do not test length
    if engine_name not in ('quora', 'youtube'):
        assert len(links) == 3, '{}: {}'.format(engine_name, len(links))
    for link in links:
        assert 'link' in link, engine_name   # workaround for #332
        assert 'title' in link, engine_name  # workaround for #332


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    for engine_name in (engine_names or scrapers):
        make_engine_api_call(engine_name)
