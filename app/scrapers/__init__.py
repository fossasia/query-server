from __future__ import absolute_import
from __future__ import print_function

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
    results = scrapers['g'].search('fossasia', 10)
    assert isinstance(results, list)
    assert len(results) == 10


def feedgen(query, engine, count=10):
    return scrapers[engine.strip().lower()].search(query, count)
