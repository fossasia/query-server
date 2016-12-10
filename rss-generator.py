import mechanize
from feedgen.feed import FeedGenerator
import urlparse
from bs4 import BeautifulSoup
import sys
import json
import os

query = ''

def generateFeed(urls):
    ''' Generates RSS feel from the given urls '''
    fg = FeedGenerator()
    fg.title('Google Search Results')
    fg.link(href='http://google.com', rel='alternate')
    fg.description('Google Seach Results')
    for url in urls:
        fe = fg.add_entry()
        fe.title(url[0])
        fe.link({'href': url[1], 'rel':'alternate'})  
    print fg.rss_str(pretty=True)  
    ##Write to file
    file_name = os.path.dirname(os.path.abspath(__file__)) + '/data/' + query + ".xml"
    fg.rss_file(file_name)
  

def google_search(query):
    ''' Search google for the query and return set of urls
    Returns: urls (list)
            [[Tile1,url1], [Title2, url2],..]
    '''
    urls = []
    response = get_results_page(query)
    soup = BeautifulSoup(response.read(), 'html.parser')
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
    query = read_in()
    ##query = "harambe"
    urls = google_search(query)
    generateFeed(urls)
if __name__ == "__main__":
    main()
