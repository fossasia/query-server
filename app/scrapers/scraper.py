import importlib
import inspect
import os

import requests
from bs4 import BeautifulSoup


class Scraper(object):
    url = ''
    startKey = ''
    queryKey = 'q'
    defaultStart = 0
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36'
            ' (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'
        )
    }

    def __init__(self):
        print('Scraper {} loaded.'.format(self.__class__.__name__))

    def get_page(self, query, startIndex=0):
        """ Fetch the google search results page
        Returns : Results Page
        """
        payload = {self.queryKey: query, self.startKey: startIndex}
        response = requests.get(self.url, headers=self.headers, params=payload)
        return response

    def parse_response(self, soup):
        raise NotImplementedError

    def next_start(self, current_start, prev_results):
        return current_start + len(prev_results)

    def search(self, query, num_results):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        current_start = self.defaultStart

        while(len(urls) < num_results):
            response = self.get_page(query, current_start)
            soup = BeautifulSoup(response.text, 'html.parser')
            new_results = self.parse_response(soup)
            if new_results is None:
                break
            urls.extend(new_results)
            current_start = self.next_start(current_start, new_results)
        return urls[:num_results]

    def search_without_count(self, query):
        """
            Search for the query and return set of urls
            Returns: list
        """
        payload = {self.queryKey: query}
        response = requests.get(self.url, headers=self.headers, params=payload)
        urls = self.parse_response(BeautifulSoup(response.text, 'html.parser'))
        return urls


# === functions dedicated to the autoloading of scrapers ===
def _is_scraper(cls):
    """cls is a class that is a subclass of Scraper but is not Scraper"""
    return (inspect.isclass(cls) and issubclass(cls, Scraper) and
            cls != Scraper)


def _get_scraper_classes():
    """Look through Python files in this directory to find all subclasses of
       Scraper"""
    dirname = os.path.dirname(os.path.abspath(__file__))
    scraper_classes = []
    for file_name in sorted(os.listdir(dirname)):
        root, ext = os.path.splitext(file_name)
        if ext.lower() == '.py':
            module = importlib.import_module('.' + root, 'scrapers')
            for _, cls in inspect.getmembers(module, _is_scraper):
                scraper_classes.append(cls)
    return scraper_classes


def get_scrapers():
    return {cls.__name__.lower(): cls for cls in _get_scraper_classes()}


if __name__ == '__main__':
    import timeit  # noqa
    timeit.timeit(get_scrapers())
