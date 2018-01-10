from __future__ import print_function
from .generalized import Scraper


class Indeed(Scraper):
    """Scrapper class for Indeed"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://www.indeed.com/jobs'
        self.defaultStart = 0

    def parse_response(self, soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a', {'class': 'turnstileLink'}):
            urls.append({'title': a.get('title'), 'link': 'https://www.indeed.com'+a.get('href')})

        print('Indeed parsed: ' + str(urls))

        return urls
