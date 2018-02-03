from __future__ import print_function
import requests
from bs4 import BeautifulSoup

VID_SCRAPERS = ('ask', 'bing', 'parsijoo', 'yahoo')
ISCH_SCRAPERS = ('bing', 'parsijoo', 'yahoo')
NEWS_SCRAPERS = ('baidu', 'bing', 'parsijoo', 'mojeek')


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
        # To avoid AttributeError when checking for self.name
        self.name = "general"

    def get_page(self, query, startIndex=0, qtype=''):
        """ Fetch the google search results page
        Returns : Results Page
        """
        url = self.url
        if qtype == 'vid' and self.name in VID_SCRAPERS:
                url = self.videoURL
        elif qtype == 'isch' and self.name in ISCH_SCRAPERS:
                url = self.imageURL
        elif qtype == 'news' and self.name in NEWS_SCRAPERS:
            url = self.newsURL

        if self.name in ('quora', 'youtube'):
            payload = {self.queryKey: query}
        else:
            payload = {self.queryKey: query, self.startKey: startIndex,
                       self.qtype: qtype}

        if self.name == 'mojeek' and qtype == 'news':
            payload['fmt'] = 'news'
        response = requests.get(url, headers=self.headers, params=payload)
        print(response)
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

    def search(self, query, num_results=10, qtype=''):
        """
            Search for the query and return set of urls
            Returns: list
        """
        urls = []
        current_start = self.defaultStart

        while (len(urls) < num_results):
            response = self.get_page(query, current_start, qtype)
            soup = BeautifulSoup(response.text, 'html.parser')
            new_results = self.call_appropriate_parser(qtype, soup)
            if new_results is None:
                break
            urls.extend(new_results)
            # Quora and youtube return all results on the same page
            if self.name in ('quora', 'youtube'):
                break
            current_start = self.next_start(current_start, new_results)

        return urls[: num_results]

    def call_appropriate_parser(self, qtype, soup):
        new_results = ''
        if qtype == 'vid' and self.name in VID_SCRAPERS:
            new_results = self.parse_video_response(soup)
        elif qtype == 'isch' and self.name in ISCH_SCRAPERS:
            new_results = self.parse_image_response(soup)
        elif qtype == 'news' and self.name in NEWS_SCRAPERS:
            new_results = self.parse_news_response(soup)
        else:
            new_results = self.parse_response(soup)
        return new_results
