from __future__ import print_function
import os, json, sys
import requests
from bs4 import BeautifulSoup

class Bing:
    def __init__(self):
        pass

    def get_page(self,query):
        """
        Fetches search response from bing.com
        returns : result page in html
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
        payload = {'q': query}
        response = requests.get('http://www.bing.com/search', params=payload, headers=header)
        return response

    def results_search(self,query):
        """ Search bing for the query and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        response = self.get_page(query)
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.findAll('li', {'class': 'b_algo'}):
            title = li.h2.text.replace('\n', '').replace('  ', '')
            url = li.h2.a['href']
            desc = li.find('p').text
            url_entry = {'title': title,
                         'link': url,
                         'desc': desc}
            urls.append(url_entry)

        return urls
