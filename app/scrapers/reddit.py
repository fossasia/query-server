import requests
from .generalized import Scraper


class Reddit(Scraper):
    """This scraper takes a query and a count and returns
    the results of a Reddit Search"""

    def __init__(self):
        Scraper.__init__(self)
        self.redditURL = 'https://reddit.com/search.json?q='

    def search(self, query, num_results, qtype=''):
        """ Makes a GET request to Reddit API and returns the URLs
        Returns: urls (list)
                [[Title1,url1], [Title2, url2],..]
        """
        url = self.redditURL + requests.utils.quote(query, safe='')
        url += '&limit={}'.format(num_results)
        
        responses = requests.get(url, headers=Scraper.headers).json()

        links = []
        for response in responses['data']['children']:
            link = 'https://www.reddit.com'+response['data']['permalink']
            links.append({'link': link, 'text': response['data']['title']})

        print('Reddit parsed: ' + str(links))

        return links
