import os, json, sys
import requests
import mechanize
from feedgen.feed import FeedGenerator
import urlparse
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
    print fg.rss_str(pretty=True)
    ##Write to file
    file_name = 'data/%s.xml'%query
    fg.rss_file(file_name)

def bing_search(query):
    ''' Search bing for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_bing_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')
    # Search for all relevant 'div' tags with having the results
    for li in soup.findAll('li', attrs = {'class' : ['b_algo']}):
       # search for title
       title = li.h2.text.replace("\n",'').replace("  ","")
       # get anchor tag having the link
       url = li.h2.a['href']
       # get the short description
       desc = li.find('p').text
       url_entry = [title, url, desc]
       urls.append(url_entry)
    return urls

def duckduckgo_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_duckduckgo_page(query)
    soup = BeautifulSoup(response.read(), 'html5lib')

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

def get_duckduckgo_page(query):
    """
    Fetch the duckduckgo search results page

    :param query:   String to be searched on duckduckgo
    :return:        Result page containing search results
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)  # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open('http://www.duckduckgo.com/html/')
    br.select_form(name='x')
    br.form['q'] = query
    return br.submit()

def get_bing_page(query):
    """
    Fetch the bing search results page

    :param query:   String to be searched on bing
    :return:        Result page containing search results
    """
    br = mechanize.Browser()
    br.set_handle_robots(False)  # Google's robot.txt prevents from scrapping
    br.addheaders = [('User-agent', 'Mozilla/5.0')]
    br.open('http://www.bing.com/search')
    formcount = 0
    for form in br.forms():
        if str(form.attrs["id"]) == "sb_form":
            break
        formcount += 1
    br.select_form(nr=formcount)
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
    elif stype == 'd':
        urls = duckduckgo_search(query)
    else:
        urls = bing_search(query)
    generateFeed(urls, stype)


if __name__ == "__main__":
    main()
