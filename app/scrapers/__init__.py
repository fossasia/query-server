from __future__ import print_function
from ask import Ask
from baidu import Baidu
from bing import Bing
from duckduckgo import Duckduckgo
from exalead import Exalead
from google import Google
from quora import Quora
from yahoo import Yahoo
from yandex import Yandex

scrapers = {
    'ask': Ask(),
    'bing': Bing(),
    'baidu': Baidu(),
    'duckduckgo': Duckduckgo(),
    'exalead': Exalead(),
    'google': Google(),
    'quora': Quora(),
    'yahoo': Yahoo(),
    'yandex': Yandex()
}


def small_test():
    assert isinstance(scrapers['google'].results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    if engine == 'quora':
        return scrapers[engine.strip().lower()].search_without_count(query, count)
    else:
        return scrapers[engine.strip().lower()].search(query, count)
