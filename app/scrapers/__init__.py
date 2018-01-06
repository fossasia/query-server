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
from .yandex import Yandex
from .youtube import Youtube

scrapers = {
    'google': Google('image')
    # 'ask': Ask(),
    # 'baidu': Baidu(),
    # 'bing': Bing(),
    # 'dailymotion': DailyMotion(),
    # 'duckduckgo': DuckDuckGo(),
    # 'exalead': ExaLead(),
    # 'google': Google(),
    # 'mojeek': Mojeek(),
    # 'parsijoo': Parsijoo(),
    # 'quora': Quora(),
    # 'yahoo': Yahoo(),
    # 'yandex': Yandex(),
    # 'youtube': Youtube()
}



def small_test():
    assert isinstance(scrapers['google'].search('fossasia',  1), list)


def feed_gen(query, engine, extra, count=10):
    print("Extra variable:", extra)
    engine = engine.lower()
    print("Engine: ", engine)
    print("Searcgh Engine", scrapers[engine])
    # provide temporary backwards compatibility for old names
    old_names = {'ubaidu': 'baidu',
                 'vdailymotion': 'dailymotion',
                 'tyoutube': 'youtube'}
    engine = old_names.get(engine, engine)
    Scarper_class = scrapers(extra)

    if engine in ('quora', 'youtube'):
        urls = Scarper_class[engine].search_without_count(query)
    else:
        urls = Scarper_class[engine].search(query, count, extra)
    return urls
