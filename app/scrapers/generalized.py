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
        url = self.url
        if qtype == 'vid':
            if self.name in ['yahoo']:
                url = self.videoURL
            elif self.name in ['ask']:
                url = self.videoURL
                payload = {self.queryKey: query, self.startKey: startIndex}
                response = requests.get(
                    url, headers=self.headers, params=payload
                )
                return response
            else:
                url = self.url
        payload = {self.queryKey: query, self.startKey: startIndex,
                   self.qtype: qtype}
        response = requests.get(url, headers=self.headers, params=payload)
        print(response.url)
        return response

    @staticmethod
    def parse_response(soup):
        raise NotImplementedError

    @staticmethod
    def parse_video_response(soup):
        raise NotImplementedError

    @staticmethod
    def next_start(current_start, prev_results):
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
            if qtype == 'vid':
                if self.name in ['yahoo']:
                    new_results = self.parse_video_response(soup)
                else:
                    new_results = self.parse_response(soup)
            else:
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

    def video_search(self, query, num_results, qtype=''):
        urls = []
        current_start = self.defaultStart

        while (len(urls) < num_results):
            response = self.get_page(query, current_start, qtype)
            soup = BeautifulSoup(response.text, 'html.parser')
            if qtype == 'vid':
                if self.name in ['yahoo', 'ask']:
                    new_results = self.parse_video_response(soup)
                else:
                    new_results = self.parse_response(soup)
            else:
                new_results = self.parse_response(soup)
            if new_results is None:
                break
            urls.extend(new_results)
            current_start = self.next_start(current_start, new_results)
        return urls[: num_results]

    def video_search_without_count(self, query):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        if self.name in ['parsijoo']:
            url = self.videoURL
            payload = {self.queryKey: query}
        elif self.name in ['bing']:
            url = self.videoURL
            payload = {self.queryKey: query, self.videoKey: 'HDRSC3'}
        response = requests.get(url, headers=self.headers, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = self.parse_video_response(soup)
        if len(urls) == 0:
            return "No video with this Keyword"
        else:
            return urls

    def image_search_without_count(self, query):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        if self.name in ['parsijoo']:
            url = self.imageURL
            payload = {self.queryKey: query}
        elif self.name in ['bing']:
            url = self.imageURL
            payload = {self.queryKey: query, self.imageKey: 'HDRSC2'}
        response = requests.get(url, headers=self.headers, params=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = self.parse_image_response(soup)
        return urls
