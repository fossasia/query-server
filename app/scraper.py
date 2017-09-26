from __future__ import print_function
import os, json, sys
import requests
from bs4 import BeautifulSoup

try:
  reload                        # Python 2
except NameError:
  from importlib import reload  # Python 3

reload(sys)

try:
    sys.setdefaultencoding('utf8')
except AttributeError:
    pass

HEADERS = {'User-Agent':
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}

search_engines = {'g': ('GOOGLE SEARCH RESULTS', 'https://www.google.com', 'Google search results for %s'),
                  'd': ('DUCKDUCKGO SEARCH RESULTS', 'https://www.duckduckgo.com', 'Duckduckgo search results for %s'),
                  'b': ('BING SEARCH RESULTS', 'https://www.bing.com', 'Bing search results for %s'),
                  'y': ('YAHOO SEARCH RESULTS', 'https://search.yahoo.com/', 'Yahoo search results for %s'),
                  'a': ('ASK SEARCH RESULTS', 'http://www.ask.com/', 'Ask search results for %s')}
query = ''


def get_bing_page(query,index):
    """
    Fetches search response from bing.com
    returns : result page in html
    """
    payload = {'q': query, 'first' : index}
    response = requests.get('http://www.bing.com/search', params=payload, headers=HEADERS)
    return response


def bing_search(query,count):
    """ Search bing for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    for index in range(10,count+1,10):
        response = get_bing_page(query,index+1)
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.findAll('li', {'class': 'b_algo'}):
            title = li.h2.text.replace('\n', '').replace('  ', '')
            url = li.h2.a['href']
            desc = li.find('p').text
            url_entry = {'title': title,
                         'link': url,
                         'desc': desc}
            urls.append(url_entry)
            if len(urls) == count:
                return urls


def get_duckduckgo_page(query):
    """
    Search query on duckduckgo
    Returns : Result page in html
    """
    response = requests.get('https://duckduckgo.com/html' + query, headers=HEADERS)
    return response


def duckduckgo_search(query, count):
    """ Search duckduckgo for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    query = '/?q=' + query
    while True:
        response = get_duckduckgo_page(query)
        soup = BeautifulSoup(response.text, 'html.parser')
        navLink = soup.find_all('div', {'class': 'nav-link'})
        if navLink:
            navLinkForm = navLink[-1].find('form', {'action': '/html/', 'method': 'post'})
            navLinkForm = navLinkForm.find_all('input')
            parameters = [(i['name']+'='+i['value']) for i in navLinkForm[1:]]
            parameters = '&'.join(parameters)

            for links in soup.findAll('a', {'class': 'result__a'}):
                desc = links.find_next('a')
                urls.append({'title': links.getText(),
                             'link': links.get('href'),
                             'desc': desc.getText()})
                if(len(urls) == count):
                    return urls
            query = '/?' + parameters
        else:
            return urls


def get_google_page(query,index):
    """ Fetch the google search results page
    Returns : Results Page
    """
    payload = {'q': query,'start' : index}
    response = requests.get('https://www.google.com/search', headers=HEADERS, params=payload)
    return response


def google_search(query,count):
    """ Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    index = 0
    while True:
        response = get_google_page(query,index)
        soup = BeautifulSoup(response.text, 'html.parser')
        for h3 in soup.findAll('h3', {'class': 'r'}):
            links = h3.find('a')
            desc = h3.find_next('span', {'class': 'st'})
            urls.append({'title': links.getText(),
                         'link': links.get('href'),
                         'desc': desc.getText()})
            if len(urls) == count:
                return urls
        index = len(urls) + 1



def get_yahoo_page(query,index):
    """ Fetch the yahoo search results
    Returns : Results Page
    """
    payload = {'p': query,'b' : index}
    response = requests.get('https://search.yahoo.com/search', headers=HEADERS, params=payload)
    return response


def yahoo_search(query,count):
    """ Gives search query to yahoo and returns the urls

    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls = []
    for index in range(0,count+1,10):
        response = get_yahoo_page(query,index+1)
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
                d = y.find_next('p')
                print(d)
                urls.append({'title': y.getText(),
                             'link': u,
                             'desc': d.getText()})
                if len(urls) == count:
                    return urls

def get_ask_page(query):
    """Fetch the ask search results
    Returns : Results Page
    """
    payload = {'q': query}
    response = requests.get('http://ask.com/web', headers=HEADERS, params=payload)
    return response


def ask_search(query):
    """ Search ask for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    """
    urls=[]
    response = get_ask_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    for div in soup.findAll('div', {'class': 'PartialSearchResults-item'}):
        title = div.div.a.text
        url = div.div.a['href']
        urls.append({'title': title, 'link': url})
    return urls


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def small_test():
    assert type(google_search('fossasia')) is list


def feedgen(query, engine,count):
    if engine == 'g':
        urls = google_search(query,count)
    elif engine == 'd':
        urls = duckduckgo_search(query, count)
    elif engine == 'y':
        urls = yahoo_search(query,count)
    elif engine == 'b':
        urls = bing_search(query,count)
    else:
        urls = ask_search(query)
    result = urls
    print(result)
    print(len(result))
    return result
