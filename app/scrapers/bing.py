from __future__ import absolute_import
from __future__ import print_function

from .generalized import Scraper


class Bing(Scraper):
    """Scrapper class for Bing"""

    def __init__(self):
        self.url = 'http://www.bing.com/search'
        self.defaultStart = 1
        self.startKey = 'first'

    def parseResponse(self, soup):
        """ Parses the reponse and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for li in soup.findAll('li', {'class': 'b_algo'}):
            title = li.h2.text.replace('\n', '').replace('  ', '')
            url = li.h2.a['href']
            desc = li.find('p').text
            url_entry = {'title': title,
                         'link': url,
                         'desc': desc}
            urls.append(url_entry)

        print('Bing parsed: ' + str(urls))

        return urls
