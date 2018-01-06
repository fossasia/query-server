from __future__ import print_function
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Generalized scraper"""
    url = ''
    startKey = ''
    queryKey = 'q'
    defaultStart = 0
    qtype = ''
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
            'Safari/537.36'
        )
    }

    def __init__(self):
        pass

    def get_page(self, query, startIndex=0, qtype=''):
        """ Fetch the google search results page
        Returns : Results Page
        """
        payload = {self.queryKey: query, self.startKey: startIndex, self.qtype: qtype}
        response = requests.get(self.url, headers=self.headers, params=payload)
        print(response.url)
        return response

    def parse_response(self, soup):
        raise NotImplementedError

    def next_start(self, current_start, prev_results):
        return current_start + len(prev_results)

    def search(self, query, num_results, qtype=''):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        current_start = self.defaultStart

        while (len(urls) < num_results):
            response = self.get_page(query, current_start, qtype)
            soup = BeautifulSoup(response.text, 'html.parser')
            new_results = self.parse_response(soup)
            if new_results is None:
                break
            urls.extend(new_results)
            current_start = self.next_start(current_start, new_results)
        return urls[: num_results]

    def search_without_count(self, query):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        payload = {self.queryKey: query}
        response = requests.get(self.url, headers=self.headers, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = self.parse_response(soup)
        return urls
