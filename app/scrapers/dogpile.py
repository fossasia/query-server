from __future__ import print_function
from generalized import Scraper


class Dogpile(Scraper):
    """Scrapper class for Dogpile"""

    def __init__(self):
        self.url = 'http://www.dogpile.com/search/web'
        self.defaultStart = 0
        self.startKey = 'qsi'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for links in soup.findAll('div', {'class': 'searchResult webResult'}):
            title = links.find('a', {'class': 'resultTitle'}).getText()
            url = links.find('a', {'class': 'resultDisplayUrl'}).getText()
            desc = links.find('div', {'class': 'resultDescription'}).getText()
            print(str(links.get('href')))
            urls.append({'title': title,
                         'link': url,
                         'desc': desc})
        print('parsed' + str(urls))
        return urls
