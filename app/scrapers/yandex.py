from __future__ import print_function
from generalized import Scraper


class Yandex(Scraper):
    """Scrapper class for Yandex"""

    def __init__(self):
        self.url = 'https://www.yandex.com/search'
        self.defaultStart = 0

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'link link_theme_normal'}):
            urls.append({'title': a.getText(), 'link': a.get('href')})

        print('parsed' + str(urls))

        return urls
