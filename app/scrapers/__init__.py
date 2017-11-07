from __future__ import print_function
import json
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

scrapers = {
    'ask': Ask(),
    'baiduu': Baidu(),
    'bing': Bing(),
    'duckduckgo': Duckduckgo(),
    'exalead': Exalead(),
    'google': Google(),
    'parsijoo': Parsijoo(),
    'quora': Quora(),
    'yahoo': Yahoo(),
    'yandex': Yandex(),
    'youtube': Youtube()
}


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert isinstance(scrapers['google'].search('fossasia'), list)


def feedgen(query, engine, count=10):
    if engine in ('quora', 'youtube'):
        urls = scrapers[engine].search_without_count(query)
    else:
        urls = scrapers[engine].search(query, count)
    return urls
