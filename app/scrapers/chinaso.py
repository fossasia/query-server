from __future__ import print_function
from generalized import Scraper


class ChinaSo(Scraper):
    """Scrapper class for ChinaSo"""

    def __init__(self):
        self.url = 'https://www.chinaso.com/search'
        self.defaultStart = 1
        self.startKey = 'c'
    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'target': '_blank'}):
            urls.append({'title': links.getText(),
			 'link': links.get('href')})
        print('ChinaSo parsed: ' + str(urls))
        return urls
