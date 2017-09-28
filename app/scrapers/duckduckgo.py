from __future__ import print_function
from generalized import Scraper


class Duckduckgo(Scraper):
    """Scrapper class for Duckduckgo"""

    def __init__(self):
        self.url = 'https://duckduckgo.com/html'
        self.defaultStart = 0
        self.startKey = 's'

    @classmethod
    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for links in soup.findAll('a', {'class': 'result__a'}):
            urls.append({'title': links.getText(),
                         'link': links.get('href')})
        print('parsed' + str(urls))
        return urls
