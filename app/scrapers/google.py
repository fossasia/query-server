from __future__ import print_function
import os, json, sys
from generalized import Scraper

class Google(Scraper):
    """Scrapper class for Google"""
    def __init__(self):
        self.url = 'https://www.google.com/search'
        self.defaultStart = 0

    @classmethod
    def nextStart(self, currentStart, prevResults):
        return currentStart + len(prevResults)

    @classmethod
    def parseResponse(self, soup):
        """
        Parses the response and returns set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for h3 in soup.findAll('h3', {'class': 'r'}):
            links = h3.find('a')
            urls.append({ 'title': links.getText(), 'link': links.get('href') })

        return urls

