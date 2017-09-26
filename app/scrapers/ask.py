from __future__ import print_function
import requests
from bs4 import BeautifulSoup

class Ask:
    """Scrapper class for Ask"""
    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def get_page(cls, query):
        """
        Fetches search response from ask.com
        returns : result page in html
        """
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'}
        payload = {'q': query}
        response = requests.get('http://ask.com/web', headers=header, params=payload)
        return response

    @classmethod
    def results_search(cls, query):
        """ Search ask for the query and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls=[]
        response = cls.get_page(query)
        soup = BeautifulSoup(response.text, 'html.parser')
        for div in soup.findAll('div', {'class': 'PartialSearchResults-item'}):
            title = div.div.a.text
            url = div.div.a['href']
            urls.append({'title': title, 'link': url})
        return urls
