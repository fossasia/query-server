"""
# Let's get pytest turned on before we start testing in earnest

from .scrapers import small_test


def test_small_test():
    small_test()
"""

from scrapers import feedgen


def test_true():
    assert True, "We have a problem!"


def test_search(search_engine='google'):
    result = feedgen('fossasia', search_engine[0], 10)
    assert isinstance(result, list)
    assert len(result) == 10
