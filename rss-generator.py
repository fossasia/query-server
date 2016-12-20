import os, json, sys
import requests
import mechanize
from feedgen.feed import FeedGenerator
import urlparse
from bs4 import BeautifulSoup


search_engines = {'g':("GOOGLE SEARCH RESULTS", "htps://www.google.com", "Google search results for %s"),
                  'd':("DUCKDUCKGO SEARCH RESULTS", "htps://www.duckduckgo.com", "Duckduckgo search results for %s")
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
    print fg.rss_str(pretty=True) 
    ##Write to file
    file_name = 'data/%s.xml'%query
    fg.rss_file(file_name)


def duckduckgo_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    SEARCH_ENDPOINT = "https://duckduckgo.com/html/"
    resp = requests.get(SEARCH_ENDPOINT, params = {'q' : query})
    soup = BeautifulSoup(resp.content, 'html5lib')

    # Search for all relevant 'div' tags with having the results
    for div in soup.findAll('div', attrs = {'class' : ['result', 'results_links', 'results_links_deep', 'web-result']}):
       # search for title
       title = div.h2.text.replace("\n",'').replace("  ","")
       # get anchor tag having the link
       url = div.h2.a['href']
       url_entry = [title, url]
       urls.append(url_entry)
    return urls


def google_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_results_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')  # using advanced html parser
    # Search for all relevant 'a' tags
    for a in soup.select('.r a'):
        parsed_url = urlparse.urlparse(a['href'])
        # Validate url
        if 'url' in parsed_url.path:
            urls.append([a.text, str(urlparse.parse_qs(parsed_url.query)['q'][0])])
    return urls

def get_results_page(query):
    ''' Fetch the google search results page
    Returns : Results Page
    '''
    br = mechanize.Browser()
    br.set_handle_robots(False) # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent','Mozilla/5.0')]
    br.open('http://www.google.com/')
    br.select_form(name='f')
    br.form['q'] = query
    return br.submit()

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    global query
    # read command from npm server
    command = read_in()
    # split the command
    stype, query = command.split('~')
    print query
    if stype == 'g':
        urls = google_search(query)
    else:
        urls = duckduckgo_search(query)
    generateFeed(urls, stype)

    
if __name__ == "__main__":
    main()
