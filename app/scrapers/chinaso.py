from __future__ import print_function
from generalized import Scraper


class ChinaSo(Scraper):
    """Scrapper class for ChinaSo"""
    def __init__(self):
        self.url = 'http://www.chinaso.com/search/pagesearch.htm'
        self.defaultStart = 0
        self.startKey = 'page'

    def nextStart(self, currentStart, prevResults):
        return currentStart + 1

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for li in soup.findAll('li', {'class': 'reItem'}):
            title = li.h2.a.text
            url = li.h2.a['href']
            if url.startswith('/search/'):
                url = 'www.chinaso.com' + str(url)
            else:
                pass
            urls.append({'title': title, 'link': url})
        print('ChinaSo parsed: ' + str(urls))
        return urls
