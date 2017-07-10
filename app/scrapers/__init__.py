from __future__ import print_function
import os, json, sys
from google import Google
from duckduckgo import Duckduckgo
from bing import Bing
from yahoo import Yahoo
import requests
from bs4 import BeautifulSoup
scrapers = {
        'google':Google(),
        'bing':Bing(),
        'yahoo':Yahoo(),
        'duckduckgo':Duckduckgo(),
    }

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert type(scrapers.google.results_search('fossasia')) is list


def feedgen(query, engine):
    if engine == 'g':
        urls = scrapers['google'].results_search(query)
    elif engine == 'd':
        urls = scrapers['duckduckgo'].results_search(query)
    elif engine == 'y':
        urls = scrapers['yahoo'].results_search(query)
    else:
        urls = scrapers['bing'].results_search(query)
    result = urls
    print(result)
    print(len(result))
    return result
