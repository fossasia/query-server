from __future__ import print_function
from generalized import Scraper


class SocialMention(Scraper):
    """Scrapper class for Ask"""
    def __init__(self):
        self.url = 'http://socialmention.com/search'
        self.defaultStart = 0
        self.startKey = 'start'

    def nextStart(self, currentStart, prevResults):
        return currentStart + 1

    def parseResponse(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for div in soup.findAll('div', {'class': 'body'}):
            title = div.h3.a.text
            url = div.h3.a['href']
            urls.append({'title': title, 'link': url})
        print('Social Mention parsed: ' + str(urls))
        return urls
