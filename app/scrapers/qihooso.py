from __future__ import print_function
from generalized import Scraper


class QihooSo(Scraper):
    """Scrapper class for Ask"""
    def __init__(self):
        self.url = 'https://www.so.com/s'
        self.defaultStart = 0
        self.startKey = 'pn'

    def nextStart(self, currentStart, prevResults):
        return currentStart + 1

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for h3 in soup.findAll('h3', {'class': 'res-title'}):
            title = h3.a.text
            url = h3.a['href']
            urls.append({'title': title, 'link': url})
        print('QihooSo parsed: ' + str(urls))
        return urls
