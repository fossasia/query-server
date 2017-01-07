
from __future__ import print_function
import os, json, sys
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup


search_engines = {'g':("GOOGLE SEARCH RESULTS", "htps://www.google.com", "Google search results for %s"),
                  'd':("DUCKDUCKGO SEARCH RESULTS", "htps://www.duckduckgo.com", "Duckduckgo search results for %s"),
                  'b': ("BING SEARCH RESULTS", "https://www.bing.com", "Bing search results for %s")
                  }

query = ''

def generateFeed(urls, stype):
    ''' Generates RSS feel from the given urls '''
    feed = search_engines[stype]

    fg = FeedGenerator()
    fg.title(feed[0])
    fg.link(href = feed[1], rel='alternate')
    fg.description(feed[2]%query)

    for url in urls:
        fe = fg.add_entry()
        fe.title(url[0])
        fe.link({'href': url[1], 'rel': 'alternate'})
    print(fg.rss_str(pretty=True))
    ##Write to file
    file_name = 'data/%s.xml'%query
    fg.rss_file(file_name)

def get_bing_page(query):
    '''
    Fetches search response from bing.com
    returns : result page in html
    '''

    header = {'User-Agent': 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    }

    payload = {'q' : query}

    response = requests.get('http://www.bing.com/search', params=payload, headers=header)

    return response

def bing_search(query):
    ''' Search bing for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_bing_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Search for all relevant 'li' tags with having the results
    for li in soup.findAll('li', {'class' : 'b_algo'}):
       # search for title
       title = li.h2.text.replace("\n",'').replace("  ","")
       # get anchor tag having the link
       url = li.h2.a['href']
       # get the short description
       desc = li.find('p').text
       url_entry = [title, url, desc]
       urls.append(url_entry)
    return urls

def get_duckduckgo_page(query):
    '''
    Search query on duckduckgo
    Returns : Result page in html
    '''

    header = {'User-Agent': 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    }

    payload = {'q' : query}
    response = requests.get('https://duckduckgo.com/html', headers=header, params=payload)

    return response

def duckduckgo_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_duckduckgo_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for all relevant 'a' tags with having the results
    for links in soup.findAll('a',{'class':'result__a'}):
        urls.append([links.getText(), links.get('href')])

    return urls

def get_google_page(query):
    ''' Fetch the google search results page
    Returns : Results Page
    '''
    header = {'User-Agent': 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36"
    }

    payload = {'q' : query}
    response = requests.get('https://www.google.com/search', headers=header, params=payload)

    return response

def google_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_google_page(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Search for all relevant 'h3' tags
    for h3 in soup.findAll('h3',{'class':'r'}):

        links = h3.find('a')
        
        urls.append([links.getText(),links.get('href')])

    return urls


def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():

    
    global query
    # read command from npm server
    command = read_in()
    # split the command
    stype, query = command.split('~')
    print(query)

    if stype == 'g':
        urls = google_search(query)
    elif stype == 'd':
        urls = duckduckgo_search(query)
    else:
        urls = bing_search(query)
    generateFeed(urls, stype)


if __name__ == "__main__":
    main()

