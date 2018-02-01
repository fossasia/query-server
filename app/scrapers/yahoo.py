from __future__ import print_function
from .generalized import Scraper
import re
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
        self.imageURL = 'https://images.search.yahoo.com/search/images'
        self.newsURL = 'https://news.search.yahoo.com/search'
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

    @staticmethod
    def parse_image_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for h in soup.findAll('li', attrs={'class': 'ld'}):
            t = h.find('a')
            r = t.get('aria-label')
            cleanr = re.compile('<.*?>')
            r = re.sub(cleanr, '', r)
            cleanl = re.compile('&#[\d]+(;)')
            r = re.sub(cleanl, '\'', r)
            img = t.find('img', attrs={'class': 'process'})
            url = img.get('data-src')
            urls.append({
                'title': r,
                'link': url
            })

        print('Yahoo parsed: ' + str(urls))

        return urls

    @staticmethod
    def parse_news_response(soup):
        """ Parse response and returns the urls
            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for div in soup.findAll('div', attrs={'class': 'dd algo NewsArticle'}):
            link = div.find('a', attrs={'class': 'fz-m'})
            descDiv = div.find('div', attrs={'class': 'compText'})
            unparsedURL = link.get('href')
            urlSearch = re.search('/RU=(.*?)/', unparsedURL, re.I)
            url = unquote(urlSearch.group(1))
            urls.append({
                'title': link.getText(),
                'link': url,
                'desc': descDiv.find('p').getText()
            })

        print('Yahoo parsed: ' + str(urls))

        return urls
