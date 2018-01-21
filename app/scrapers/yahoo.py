from __future__ import print_function
from .generalized import Scraper

try:
    from urllib.parse import unquote  # Python 3
except ImportError:
    from urllib import unquote        # Python 2


class Yahoo(Scraper):
    """Scrapper class for Yahoo"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://search.yahoo.com/search'
        self.videoURL = 'https://video.search.yahoo.com/search/video'
        self.defaultStart = 1
        self.startKey = 'b'
        self.name = 'yahoo'

    @staticmethod
    def parse_response(soup):
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

        return urls

    @staticmethod
    def parse_video_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for h in soup.findAll('li', attrs={'class': 'vr vres'}):
            t = h.find('a', attrs={'class': 'ng'})
            r = t.get('data-rurl')
            titleDiv = t.find('div', attrs={'class': 'v-meta bx-bb'})
            title = titleDiv.find('h3').getText()
            urls.append({
                'title': title,
                'link': r
            })

        print('Yahoo parsed: ' + str(urls))

        return urls
