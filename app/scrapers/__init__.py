from __future__ import print_function
import json
import sys
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask
from yandex import Yandex

scrapers = {
    'g': Google(),
    'b': Bing(),
    'y': Yahoo(),
    'd': Duckduckgo(),
    'a': Ask(),
    'yd': Yandex()
}


def small_test():
    assert isinstance(scrapers['g'].results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    urls = scrapers[engine].search(query, count)
    return urls
