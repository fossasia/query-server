from __future__ import print_function
from .generalized import Scraper


class Youtube(Scraper):
    """Scraper class for Youtube"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://www.youtube.com/results'
        self.queryKey = 'search_query'

    def parse_response(self, soup):
        """ Parse the response and return list of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for a in soup.findAll('a'):
            if a.get('href').startswith('/watch?'):
                link = 'https://www.youtube.com' + str(a.get('href'))
                if not a.getText().startswith('\n\n'):
                    urls.append({'title': a.getText(), 'link': link})
            else:
                continue

        print('Youtube parsed: ' + str(urls))

        return urls
