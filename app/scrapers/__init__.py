from __future__ import print_function

from ask import Ask
from baidu import Baidu
from bing import Bing
from duckduckgo import Duckduckgo
from exalead import Exalead
from google import Google
from mojeek import Mojeek
from parsijoo import Parsijoo
from quora import Quora
from yahoo import Yahoo
from yandex import Yandex
from youtube import Youtube

scrapers = {
    'a': Ask(),
    'b': Bing(),
    'd': Duckduckgo(),
    'e': Exalead(),
    'g': Google(),
    'm': Mojeek(),
    'p': Parsijoo(),
    'q': Quora(),
    't': Youtube(),
    'u': Baidu(),
    'y': Yahoo(),
    'yd': Yandex()
}


def small_test():
    assert isinstance(scrapers['g'].search('fossasia'), list)


def feedgen(query, engine, count=10):
    if engine in ('q', 't'):
        urls = scrapers[engine].search_without_count(query)
    else:
        urls = scrapers[engine].search(query, count)
    return urls
