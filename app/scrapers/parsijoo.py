from __future__ import print_function
from .generalized import Scraper
try:
    from urllib.parse import unquote  # Python 3
except ImportError:
    from urllib import unquote        # Python 2


class Parsijoo(Scraper):
    """Scraper class for Parsijoo"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://parsijoo.ir/web'
        self.newsURL = 'http://khabar.parsijoo.ir/search/'
        self.defaultStart = 0
        self.newsStart = 1
        self.startKey = 'co'
        self.name = 'parsijoo'

    @staticmethod
    def parse_response(soup):
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

    @staticmethod
    def parse_news_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for div in soup.findAll('div', {'class': 'news-title-link'}):
            title = div.a.getText()
            link = unquote(div.a.get('href'))
            urls.append({'title': title, 'link': link})

        print('Baidu parsed: ' + str(urls))

        return urls
