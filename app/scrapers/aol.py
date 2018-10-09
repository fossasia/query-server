from __future__ import print_function
from .generalized import Scraper


class Aol(Scraper):
    """Scrapper class for Aol"""
    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://search.aol.com/aol/search'
        self.defaultStart = 1
        self.startKey = 'b'
        self.name = 'aol'

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        if soup.find('ol', class_='adultRegion'):
            return None

        ol = soup.find('ol', class_='searchCenterMiddle')
        for li in ol.findAll('li', recursive=False):
            if 'class' in li.div.attrs and \
                ('Video' in li.div.attrs['class'] or
                    'Img' in li.div.attrs['class'] or
                    'SrLbl' in li.div.attrs['class']):
                continue

            title = li.div.div.h3.text
            url = li.div.div.span.text
            urls.append({'title': title, 'link': url})

        print('Aol parsed: ' + str(urls))

        return urls
