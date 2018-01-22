from __future__ import print_function
from .generalized import Scraper


class DuckDuckGo(Scraper):
    """Scrapper class for DuckDuckGo"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://duckduckgo.com/html'
        self.defaultStart = 0
        self.startKey = 's'
        self.name = 'duckduckgo'

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for links in soup.findAll('a', {'class': 'result__a'}):
            urls.append({'title': links.getText(),
                         'link': links.get('href')})

        print('DuckDuckGo parsed: ' + str(urls))

        return urls
