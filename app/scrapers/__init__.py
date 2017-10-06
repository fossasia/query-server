from __future__ import absolute_import
from __future__ import print_function
from .ask import Ask
from .bing import Bing
from .duckduckgo import Duckduckgo
from .google import Google
from .yahoo import Yahoo

scrapers = {
    'ask': Ask(),
    'bing': Bing(),
    'duckduckgo': Duckduckgo(),
    'google': Google(),
    'yahoo': Yahoo()
}


def small_test():
    assert isinstance(scrapers['google'].results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    urls = scrapers[engine.lower()].search(query, count)
    return urls
