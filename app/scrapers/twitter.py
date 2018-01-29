import requests
from .generalized import Scraper


class Twitter(Scraper):
    """This scraper takes a query and a count and returns the results of
         a Twitter search which is executed via the Loklak API"""

    def __init__(self):
        Scraper.__init__(self)
        self.loklakURL = 'http://api.loklak.org/api/search.json?q='

    def search(self, query, num_results, qtype=''):
        """ Makes a GET request to Loklak API and returns the URLs
        Returns: urls (list)
                [[Title1,url1], [Title2, url2],..]
        """
        url = self.loklakURL+query

        responses = requests.get(url).json()

        tweets = []
        for response in responses['statuses']:
            tweets.append({'link': response['link'], 'text': response['text']})

        print('Twitter parsed: ' + str(tweets))

        return tweets[:num_results]
