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
from mojeek import Mojeek
from chinaso import ChinaSo
from dailymotion import Dailymotion

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
    'm': Mojeek(),
    'c': ChinaSo(),
    'v': Dailymotion()
}


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert isinstance(scrapers.google.results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    if engine in ['q', 't']:
        urls = scrapers[engine].search_without_count(query)
    else:
        urls = scrapers[engine].search(query, count)
    return urls
