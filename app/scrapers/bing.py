from __future__ import print_function
from .generalized import Scraper


class Bing(Scraper):
    """Scrapper class for Bing"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'http://www.bing.com/search'
        self.videoURL = 'https://www.bing.com/videos/search'
        self.imageURL = 'https://www.bing.com/images/search'
        self.defaultStart = 1
        self.startKey = 'first'
        self.name = 'bing'

    @staticmethod
    def parse_response(soup):
        """ Parses the reponse and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for li in soup.findAll('li', {'class': 'b_algo'}):
            title = li.h2.text.replace('\n', '').replace('  ', '')
            url = li.h2.a['href']
            desc = li.find('p').text
            url_entry = {'title': title,
                         'link': url,
                         'desc': desc}
            urls.append(url_entry)

        print('Bing parsed: ' + str(urls))

        return urls

    @staticmethod
    def parse_video_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for a in soup.findAll('a', attrs={'class': 'mc_vtvc_link'}):
            title = a.get('aria-label').split(' Duration')[0]
            url = 'https://www.bing.com' + a.get('href')
            urls.append({
                'title': title,
                'link': url
            })

        print('Bing parsed: ' + str(urls))

        return urls

    @staticmethod
    def parse_image_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[url1], [url2], ...]
        """
        urls = []
        for a in soup.findAll('a', attrs={'class': 'iusc'}):
            url = 'https://www.bing.com' + a.get('href')
            urls.append({
                'link': url
            })

        print('Bing parsed: ' + str(urls))

        return urls
