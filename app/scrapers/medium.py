from __future__ import print_function
from generalized import Scraper
import requests
from bs4 import BeautifulSoup


class Medium(Scraper):
    """Scrapper class for Medium"""
    
    def __init__(self):
        self.url = 'https://www.medium.com/search/posts?q='
        self.keyword = 'q'
        self.count = 'resp'

    def search(self, query, count):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        site = requests.get(self.url + query + "&count=" + str(count))
        data = site.content.decode('utf-8')
        b_soup = BeautifulSoup(data, 'lxml')
        container = b_soup.find_all("div", {"class": "postArticle-content"})
        
        for item in container:
            title = item.find("h3")
            link = item.find("a")['href']
            urls.append({'title': title.text.strip(), 'link': link.strip()})
        print('Medium parsed: ' + str(urls))
        
        return urls

       