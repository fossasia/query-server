from __future__ import print_function

from .ask import Ask
from .baidu import Baidu
from .bing import Bing
from .dailymotion import DailyMotion
from .duckduckgo import DuckDuckGo
from .exalead import ExaLead
from .google import Google
from .mojeek import Mojeek
from .parsijoo import Parsijoo
from .quora import Quora
from .yahoo import Yahoo
from .youtube import Youtube

scrapers = {
    'ask': Ask(),
    'baidu': Baidu(),
    'bing': Bing(),
    'dailymotion': DailyMotion(),
    'duckduckgo': DuckDuckGo(),
    'exalead': ExaLead(),
    'google': Google(),
    'mojeek': Mojeek(),
    'parsijoo': Parsijoo(),
    'quora': Quora(),
    'yahoo': Yahoo(),
    'youtube': Youtube()
}


def small_test():
    assert isinstance(scrapers['google'].search('fossasia', 1), list)


def feed_gen(query, engine, count=10, qtype=''):
    engine = engine.lower()
    # provide temporary backwards compatibility for old names
    old_names = {'ubaidu': 'baidu',
                 'vdailymotion': 'dailymotion',
                 'tyoutube': 'youtube'}
    engine = old_names.get(engine, engine)
    if engine in ('quora', 'youtube'):
        urls = scrapers[engine].search_without_count(query)
    elif engine in ('baidu',) and qtype == 'news':
        urls = scrapers[engine].news_search(query, count, qtype)
    else:
        urls = scrapers[engine].search(query, count, qtype)
    return urls
