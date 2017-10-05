from __future__ import print_function
import json
import sys
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask
from aol import AOL

scrapers = {
    'google': Google(),
    'bing': Bing(),
    'yahoo': Yahoo(),
    'duckduckgo': Duckduckgo(),
    'ask': Ask(),
    'aol': AOL()
}


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert isinstance(scrapers.google.results_search('fossasia'), list)


def feedgen(query, engine, count=10):
    urls = scrapers[engine].search(query, count)
    return urls
