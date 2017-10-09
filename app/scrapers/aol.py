from __future__ import print_function
from generalized import Scraper


class AOL(Scraper):
    """Scrapper class for AOL"""

    def __init__(self):
        self.url = 'http://search.aol.com/aol/search'
        self.defaultStart = 1
        self.startKey = 'page'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'find'}):
            urls.append({'title': a.getText(), 'link': a.get('href')})

        print('parsed' + str(urls))

        return urls
