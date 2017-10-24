from __future__ import print_function
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask
from yandex import Yandex
from baidu import Baidu

scrapers = {
    'g': Google(),
    'b': Bing(),
    'y': Yahoo(),
    'd': Duckduckgo(),
    'a': Ask(),
    'yd': Yandex(),
    'u': Baidu()
}


def small_test():
    results = scrapers['g'].search('fossasia', 10)
    assert isinstance(results, list)
    assert len(results) == 10


def feedgen(query, engine, count=10):
    urls = scrapers[engine].search(query, count)
    return urls
