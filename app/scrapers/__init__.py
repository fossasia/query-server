from __future__ import print_function

from ask import Ask
from baidu import Baidu
from bing import Bing
from dailymotion import Dailymotion
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
    'ask': Ask(),
    'baidu': Baidu(),
    'bing': Bing(),
    'dailymotion': Dailymotion(),
    'duckduckgo': Duckduckgo(),
    'exalead': Exalead(),
    'google': Google(),
    'mojeek': Mojeek(),
    'parsijoo': Parsijoo(),
    'quora': Quora(),
    'yahoo': Yahoo(),
    'yandex': Yandex(),
    'youtube': Youtube()
}

# provide temporary backwards compatibility for old names
old_names = {'ubaidu': 'baidu',
             'vdailymotion': 'dailymotion',
             'tyoutube': 'youtube'}


def small_test():
    assert isinstance(scrapers['google'].search('fossasia', 1), list)


def get_scraper(engine_name):
    print(engine_name)
    engine_name = engine_name.lower()
    print(engine_name)
    return scrapers[old_names.get(engine_name, engine_name)]


def feedgen(query, engine_name, count=10):
    scraper = get_scraper(engine_name)
    if engine_name in ('quora', 'youtube'):
        urls = scraper.search_without_count(query)
    else:
        urls = scraper.search(query, count)
    return urls
