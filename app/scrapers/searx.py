from __future__ import print_function
from .generalized import Scraper

class Searx(Scraper):
    """Scraper class for Searx search"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://searx.me/'
        self.defaultStart = 0
        self.name = 'searx'

    @staticmethod
    def parse_response(soup):
        """
        Parses the response and returns the set of urls
        Returns: urls(list)
                [[Title1, url1], [Title2, url2],..]
        """
        urls = []
        for h4 in soup.findAll('h4', {'class': 'result_header'}):
            links = h4.find('a')
            urls.append({'title': links.getText(), 'link': links.get('href')})

        print('Searx parsed: ' + str(urls))

        return urls
