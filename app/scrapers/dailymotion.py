from __future__ import print_function
from .generalized import Scraper
import json


class Dailyion(Scraper):
    """Scraper class for DailyMotion"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'https://api.dailymotion.com/videos/'
        self.queryKey = 'search'
        self.startKey = 'page'
        self.defaultStart = 1
        self.name = 'dailymotion'

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []

        video_list = json.loads(str(soup))['list']

        for item in video_list:
            title = item['title']
            link = 'https://www.dailymotion.com/video/' + str(item['id'])
            urls.append({'title': title, 'link': link})

        print('Dailymotion parsed: ' + str(urls))

        return urls
