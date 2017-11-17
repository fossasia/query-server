from __future__ import print_function
from generalized import Scraper


class Mojeek(Scraper):
    """Scraper class for Mojeek"""

    def __init__(self):
        self.url = 'https://www.mojeek.co.uk/search'
        self.defaultStart = 1
        self.startKey = 's'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'ob'}):
            title = a.getText()
            url = a.get('href')
            urls.append({'title': title, 'link': url})

        print('Mojeek parsed: ' + str(urls))

        return urls
