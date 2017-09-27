from __future__ import print_function
import requests
from bs4 import BeautifulSoup


class Duckduckgo:
    """Scrapper class for Duckduckgo"""
    def __init__(self):
        pass

    def get_page(self, query):
        """
        Search query on duckduckgo
        Returns : Result page in html
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
        payload = {'q': query}
        response = requests.get('https://duckduckgo.com/html', headers=header, params=payload)
        return response

    def results_search(self, query):
        """ Search google for the query and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        response = self.get_page(query)
        soup = BeautifulSoup(response.text, 'html.parser')
        for links in soup.findAll('a', {'class': 'result__a'}):
            urls.append({'title': links.getText(),
                         'link': links.get('href')})

        return urls
