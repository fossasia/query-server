from __future__ import print_function
from .scraper import Scraper
try:
    from urllib.parse import unquote  # Python 3
except ImportError:
    from urllib import unquote        # Python 2


class Yahoo(Scraper):
    """Scrapper class for Yahoo"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://search.yahoo.com/search'
        self.defaultStart = 1
        self.startKey = 'b'

    def parse_response(self, soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for h in soup.findAll('h3', attrs={'class': 'title'}):
            t = h.findAll('a', attrs={'class': ' ac-algo fz-l ac-21th lh-24'})
            for y in t:
                r = y.get('href')
                f = r.split('RU=')
                e = f[-1].split('/RK=2')
                u = unquote(e[0])
                urls.append({
                    'title': y.getText(),
                    'link': u
                })

        print('Yahoo parsed: ' + str(urls))
        print(type(urls), urls)
        for i, item in enumerate(urls):
            print(i, item)
            for key, value in item.items():
                print(i, type(key), type(value), key, value)
        print(type(urls), urls)
        print('-' * 20)

        return urls
