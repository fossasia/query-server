from __future__ import print_function
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask
from yandex import Yandex

scrapers = {
    'ask': Ask(),
    'bing': Bing(),
    'duckduckgo': Duckduckgo(),
    'google': Google(),
    'yahoo': Yahoo(),
    'yandex': Yandex()
}


def small_test():
    assert isinstance(scrapers['google'].results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    return scrapers[engine.lower()].search(query, count)
