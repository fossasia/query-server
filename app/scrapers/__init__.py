from __future__ import print_function
import os
import json
import sys
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
from ask import Ask

scrapers = {
    'g': Google(),
    'b': Bing(),
    'y': Yahoo(),
    'd': Duckduckgo(),
    'a': Ask()
}

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def small_test():
    assert type(scrapers.google.results_search('fossasia')) is list

def feedgen(query, engine, count = 10):
    urls = scrapers[engine].search(query, count)
    print(urls)
    print(len(urls))
    return urls
