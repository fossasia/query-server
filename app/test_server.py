from __future__ import absolute_import

from .scrapers import feedgen, small_test


def test_true():
    assert True, "We have a problem!"


def test_search(search_engine='google'):
    result = feedgen('fossasia', search_engine[0], 10)
    assert isinstance(result, list)
    assert len(result) == 10


def test_small_test():
    small_test()
