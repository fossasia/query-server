from __future__ import print_function
import os, json, sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
search_engines = {'g': ('GOOGLE SEARCH RESULTS', 'htps://www.google.com', 'Google search results for %s'),
                  'd': ('DUCKDUCKGO SEARCH RESULTS', 'htps://www.duckduckgo.com', 'Duckduckgo search results for %s'),
                  'b': ('BING SEARCH RESULTS', 'https://www.bing.com', 'Bing search results for %s'),
                  'y': ('YAHOO SEARCH RESULTS', 'https://search.yahoo.com/', 'Yahoo search results for %s'),
                  'a': ('ASK SEARCH RESULTS','http://www.ask.com/','Ask search results for %s')}
query = ''


def get_ask_page(query):
    """
    Fetches search response from ask.com
    returns : result page in html
    """

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query}
    response = requests.get('http://www.ask.com/web', params=payload, headers=header)
    return response

def ask_search(query):
    """ Search bing for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls=[]
    #response = requests.get('http://www.ask.com/web', params=payload, headers=header,proxies=proxyDict)
    response = get_ask_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    for div in soup.findAll('div', {'class': 'PartialSearchResults-item'}):
        title = div.div.a.text
        url = div.div.a['href']
        url_entry = {'title': title,
                     'link': url}
        urls.append(url_entry)

    return urls

def get_bing_page(query):
    """
    Fetches search response from bing.com
    returns : result page in html
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query}
    response = requests.get('http://www.bing.com/search', params=payload, headers=header)
    return response


def bing_search(query):
    """ Search bing for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    response = get_bing_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    for li in soup.findAll('li', {'class': 'b_algo'}):
        title = li.h2.text.replace('\n', '').replace('  ', '')
        url = li.h2.a['href']
        desc = li.find('p').text
        url_entry = {'title': title,
                     'link': url,
                     'desc': desc}
        urls.append(url_entry)

    return urls


def get_duckduckgo_page(query):
    """
    Search query on duckduckgo
    Returns : Result page in html
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query}
    response = requests.get('https://duckduckgo.com/html', headers=header, params=payload)
    return response


def duckduckgo_search(query):
    """ Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    response = get_duckduckgo_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    for links in soup.findAll('a', {'class': 'result__a'}):
        urls.append({'title': links.getText(),
                     'link': links.get('href')})

    return urls


def get_google_page(query):
    """ Fetch the google search results page
    Returns : Results Page
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query}
    response = requests.get('https://www.google.com/search', headers=header, params=payload)
    return response

def get_google_page(query,startIndex):
    """ Fetch the google search results page
    Returns : Results Page
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query,'start':startIndex}
    response = requests.get('https://www.google.com/search', headers=header, params=payload)
    return response


def google_search(query):
    """ Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    for count in range(0,10):
        response = get_google_page(query,count*10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for h3 in soup.findAll('h3', {'class': 'r'}):
            links = h3.find('a')
            urls.append({'title': links.getText(),
                         'link': links.get('href')})

    return urls


def get_yahoo_page(query):
    """ Fetch the yahoo search results
    Returns : Results Page
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
    payload = {'q': query}
    response = requests.get('https://search.yahoo.com/search', headers=header, params=payload)
    return response


def yahoo_search(query):
    """ Gives search query to yahoo and returns the urls

    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    response = get_yahoo_page(query)
    soup = BeautifulSoup(response.content, 'lxml')
    for h in soup.findAll('h3', attrs={'class': 'title'}):
        t = h.findAll('a', attrs={'class': ' ac-algo fz-l ac-21th lh-24'})
        for y in t:
            r = y.get('href')
            f = r.split('RU=')
            e = f[-1].split('/RK=0')
            g = e[-1].split('/RK=1')
            u = g[0].replace('%3a', ':').replace('%2f', '/').replace('%28', '(').replace('%29', ')').replace('%3f',
                                                                                                             '?').replace(
                '%3d', '=').replace('%26', '&').replace('%29', ')').replace('%26', "'").replace('%21', '!').replace(
                '%23', '$').replace('%40', '[').replace('%5b', ']')
            urls.append({'title': y.getText(),
                         'link': u})

    return urls


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert type(google_search('fossasia')) is list


def feedgen(query, engine):
    if engine == 'g':
        urls = google_search(query)
    elif engine == 'd':
        urls = duckduckgo_search(query)
    elif engine == 'y':
        urls = yahoo_search(query)
    elif engine == 'b':
        urls = bing_search(query)
    else:
        urls = ask_search(query)
    result = urls
    print(result)
    print(len(result))
    return result
