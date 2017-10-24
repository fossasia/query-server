from __future__ import print_function
from generalized import Scraper


class Baidu(Scraper):
    """Scrapper class for Baidu"""

    def __init__(self):
        self.url = 'https://www.baidu.com/s'
        self.defaultStart = 1
        self.queryKey = 'wd'
        self.startKey = 'pn'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for h3 in soup.findAll('h3', attrs={'class': 't c-title-en'}):
            title = h3.a.getText()
            url = h3.a.get('href')
            urls.append({'title': title, 'link': url})

        print('parsed' + str(urls))

        return urls
