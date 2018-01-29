from __future__ import print_function
from .generalized import Scraper


class Mojeek(Scraper):
    """Scraper class for Mojeek"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://www.mojeek.co.uk/search'
        self.newsURL = 'https://www.mojeek.co.uk/search'
        self.defaultStart = 1
        self.startKey = 's'
        self.name = 'mojeek'

    @staticmethod
    def parse_response(soup):
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

    @staticmethod
    def parse_news_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[url1], [url2], ...]
        """
        urls = []
        for a in soup.findAll('a', attrs={'class': 'ob'}):
            title = a.getText()
            url = a.get('href')
            urls.append({
                'title': title,
                'link': url
            })

        print('Mojeek parsed: ' + str(urls))

        return urls
