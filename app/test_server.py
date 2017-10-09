"""
# Let's get pytest turned on before we start testing in earnest

from .scrapers import small_test


def test_small_test():
    small_test()
"""


def test_true():
    assert True, "We have a problem!"
