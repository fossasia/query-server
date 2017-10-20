from __future__ import absolute_import
from __future__ import print_function
from .generalized import Scraper


class Duckduckgo(Scraper):
    """Scrapper class for Duckduckgo"""

    def __init__(self):
        self.url = 'https://duckduckgo.com/html'
        self.defaultStart = 0
        self.startKey = 's'

    def parseResponse(self, soup):
        """ Parse the response and return list of url dicts
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = [{'title': link.getText(), 'link': link.get('href')}
                for link in soup.find_all('a', class_='result__a')]
        print('parsed: ' + str(urls))
        return urls
