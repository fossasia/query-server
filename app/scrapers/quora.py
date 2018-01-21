from __future__ import print_function
from .generalized import Scraper


class Quora(Scraper):
    """Scrapper class for Quora"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://www.quora.com/search'
        self.name = 'quora'

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'question_link'}):
            link = 'https://www.quora.com' + str(a.get('href'))
            urls.append({'title': a.getText(), 'link': link})

        print('Quora parsed: ' + str(urls))

        return urls
