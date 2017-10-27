from __future__ import absolute_import

from .ask import Ask
from .baidu import Baidu
from .bing import Bing
from .duckduckgo import Duckduckgo
from .google import Google
from .yahoo import Yahoo
from .yandex import Yandex

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
    assert isinstance(scrapers['g'].search('fossasia'), list)


def feedgen(query, engine, count=10):
    return scrapers[engine.strip().lower()].search(query, count)
