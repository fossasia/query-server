from __future__ import print_function
from generalized import Scraper


class Parsijoo(Scraper):
    """Scraper class for Parsijoo"""

    def __init__(self):
        self.url = 'https://parsijoo.ir/web'
        self.defaultStart = 0
        self.startKey = 'co'

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for div in soup.findAll('div', {'class': 'result'}):
            result_title = div.find('span', {'class': 'result-title'})
            title = result_title.getText()[23:-1]
            link = result_title.find('a').get('href')
            desc = div.find('span', {'class': 'result-desc'}).getText()[35:-1]
            urls.append({'title': title, 'link': link, 'desc': desc})

        print('Parsijoo parsed: ' + str(urls))

        return urls
