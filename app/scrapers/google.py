from __future__ import absolute_import
from __future__ import print_function

from .generalized import Scraper


class Google(Scraper):
    """Scrapper class for Google"""

    def __init__(self):
        self.url = 'https://www.google.com/search'
        self.defaultStart = 0

    def nextStart(self, currentStart, prevResults):
        return currentStart + len(prevResults)

    def parseResponse(self, soup):
        """
        Parses the response and returns set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for h3 in soup.findAll('h3', {'class': 'r'}):
            links = h3.find('a')
            urls.append({'title': links.getText(), 'link': links.get('href')})

        print('Google parsed: ' + str(urls))

        return urls
