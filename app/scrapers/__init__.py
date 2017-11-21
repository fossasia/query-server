from __future__ import print_function
import sys
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask
from yandex import Yandex
from baidu import Baidu
from exalead import Exalead
from quora import Quora
from youtube import Youtube
from parsijoo import Parsijoo
from mojeek import Mojeek

scrapers = {
    'g': Google(),
    'b': Bing(),
    'y': Yahoo(),
    'd': Duckduckgo(),
    'a': Ask(),
    'yd': Yandex(),
    'u': Baidu(),
    'e': Exalead(),
    'q': Quora(),
    't': Youtube(),
    'p': Parsijoo(),
    'm': Mojeek()
}


def small_test():
    assert isinstance(scrapers['g'].search('fossasia'), list)


def feedgen(query, engine, count=10):
    if engine in ['q', 't']:
        urls = scrapers[engine].search_without_count(query)
    else:
        urls = scrapers[engine].search(query, count)
    return urls
