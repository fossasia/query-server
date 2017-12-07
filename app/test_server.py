import os

import pytest
import requests

from .scrapers import scrapers, small_test
from .scrapers.generalized import Scraper

REASON = 'Do you have query-server running on http://127.0.0.1:7001 ?'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


def test_true():
    assert True, "We have a problem!"


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_small_test():
    small_test()


@pytest.mark.xfail
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    assert response.status_code == 404


def make_engine_api_call(engine_name):
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    assert requests.get(url).status_code == 400, url

    if engine_name in ('dailymotion', 'exalead', 'mojeek', 'yandex'):
        return  # These engines need to be fixed so that they pass this test
    fmt = 'http://localhost:7001/api/v1/search/{}?query=fossaisa&num=3'
    response = requests.get(fmt.format(engine_name))
    assert response.status_code == 200, '{}: {}'.format(engine_name,
                                                        response.status_code)
    links = response.json()
    # These engines run in search_without_count() mode so we do not test length
    if engine_name not in ('quora', 'youtube'):
        assert len(links) == 3, '{}: {}'.format(engine_name, len(links))
    for link in links:
        assert 'link' in link, engine_name
        assert 'title' in link, engine_name


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    for engine_name in (engine_names or scrapers):
        make_engine_api_call(engine_name)


def test_scrapers_keys():
    assert all(isinstance(key, str) for key in scrapers.keys())


def test_scrapers_values():
    assert all(isinstance(value, Scraper) for value in scrapers.values())


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_scraper(capsys, engine_name='ask'):
    if engine_name in ('dailymotion', 'yandex'):
        return  # These engines need to be fixed so that they pass this test
    links = scrapers[engine_name].search('fossasia', 3)
    assert isinstance(links, list)
    assert len(links) == 3
    assert all('link' in link for link in links), engine_name
    assert all('title' in link for link in links), engine_name


@pytest.mark.xfail(reason='scraper names are case sensitive')
def test_scraper_upper(engine_name='ASK'):
    test_scraper(engine_name.upper())


def test_scrapers(capsys, engine_names=None):
    if not TRAVIS_CI:
        for engine_name in engine_names or scrapers.keys():
            test_scraper(engine_name)


@pytest.mark.xfail(reason='these should all fail')
def test_bad_scrapers(engine_names=None):
    test_scrapers(engine_names or ('asked', 'google+', 'zulu'))
