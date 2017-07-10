from __future__ import print_function
import os, json, sys
import requests
from bs4 import BeautifulSoup


class Yahoo:
    def __init__(self):
        pass

    def get_page(self,query):
        """ Fetch the yahoo search results
        Returns : Results Page
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
        payload = {'q': query}
        response = requests.get('https://search.yahoo.com/search', headers=header, params=payload)
        return response

    def results_search(self,query):
        """ Gives search query to yahoo and returns the urls

        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        response = self.get_page(query)
        soup = BeautifulSoup(response.content, 'lxml')
        for h in soup.findAll('h3', attrs={'class': 'title'}):
            t = h.findAll('a', attrs={'class': ' ac-algo fz-l ac-21th lh-24'})
            for y in t:
                r = y.get('href')
                f = r.split('RU=')
                e = f[-1].split('/RK=0')
                u = e[0].replace('%3a', ':').replace('%2f', '/').replace('%28', '(').replace('%29', ')').replace('%3f',
                                                                                                                 '?').replace(
                    '%3d', '=').replace('%26', '&').replace('%29', ')').replace('%26', "'").replace('%21', '!').replace(
                    '%23', '$').replace('%40', '[').replace('%5b', ']')
                urls.append({'title': y.getText(),
                             'link': u})

        return urls
