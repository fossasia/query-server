import requests
from bs4 import BeautifulSoup

class Google:
    """Scrapper class for Google"""
    def __init__(self):
        pass


    def get_page(self, query):
        """ Fetch the google search results page
        Returns : Results Page
        """
        header = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) ' 
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')}
        payload = {'q': query}
        response = requests.get('https://www.google.com/search',
            headers = header, params = payload)
        return response


    def get_page(self, query, startIndex):
        """ Fetch the google search results page
        Returns : Results Page
        """
        header = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')}
        payload = {'q': query, 'start': startIndex}
        response = requests.get('https://www.google.com/search',
            headers = header, params = payload)
        return response


    def results_search(self, query):
        """ Search google for the query and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for count in range(0, 10):
            response = self.get_page(query, count * 10)
            soup = BeautifulSoup(response.text, 'html.parser')
            for h3 in soup.findAll('h3', {'class': 'r'}):
                links = h3.find('a')
                urls.append({'title': links.getText(),
                             'link': links.get('href')})

        return urls

