from __future__ import print_function
from .generalized import Scraper


class Parsijoo(Scraper):
    """Scraper class for Parsijoo"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://parsijoo.ir/web'
        self.imageURL = 'https://image.parsijoo.ir/image'
        self.videoURL = 'https://video.parsijoo.ir/video'
        self.defaultStart = 0
        self.startKey = 'co'
        self.name = 'parsijoo'

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        for div in soup.findAll('div', {'class': 'result'}):
            result_title = div.find('span', {'class': 'result-title'})
            title = result_title.getText()[23:-1]
            link = result_title.find('a').get('href')
            desc = div.find('span', {'class': 'result-desc'}).getText()[35:-1]
            urls.append({'title': title, 'link': link, 'desc': desc})

        print('Parsijoo parsed: ' + str(urls))

        return urls

    @staticmethod
    def parse_video_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for a in soup.findAll('a', attrs={'class': 'over-page'}):
            title = a.get('title')
            url = 'https://video.parsijoo.ir' + a.get('href')
            urls.append({
                'title': title,
                'link': url
            })

        print('Parsijoo parsed: ' + str(urls))

        return urls

    @staticmethod
    def parse_image_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[url1], [url2], ...]
        """
        urls = []
        for div in soup.findAll('div', attrs={'class': 'image-container overflow'}):
            a = div.find('a')
            url = 'https://image.parsijoo.ir' + a.get('href')
            urls.append({
                'link': url
            })

        print('Parsijoo parsed: ' + str(urls))

        return urls
