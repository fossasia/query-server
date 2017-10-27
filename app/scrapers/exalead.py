from __future__ import print_function
from generalized import Scraper


class Exalead(Scraper):
    """Scraper class for Exalead"""

    def __init__(self):
        self.url = 'https://www.exalead.com/search/web/results/'
        self.defaultStart = 0
        self.startKey = 'start_index'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'title'}):
            urls.append({
                'title': a.getText(),
                'link': a.get('href')
                })
        print('Exalead parsed: ' + str(urls))
        return urls
