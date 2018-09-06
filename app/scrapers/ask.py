from __future__ import print_function
from .generalized import Scraper


class Ask(Scraper):
    """Scrapper class for Ask"""

    def __init__(self):
        Scraper.__init__(self)
        self.url = 'http://ask.com/web'
        self.videoURL = 'https://www.ask.com/youtube'
        self.defaultStart = 1
        self.startKey = 'page'
        self.name = 'ask'

    @staticmethod
    def next_start(current_start, prev_results):
        return current_start + 1

    @staticmethod
    def parse_response(soup):
        """ Parse the response and return set of urls
        Returns: urls (list)
                [[Tile1,url1], [Title2, url2],..]
        """
        urls = []
        if soup.find('div', class_='PartialSearchResults-noresults'):
            return None
        for div in soup.findAll('div', class_='PartialSearchResults-item'):
            title = div.div.a.text
            url = div.div.a['href']
            try:
                p = div.find('p', class_='PartialSearchResults-item-abstract')
                desc = p.text.replace('\n', '')
                urls.append({'title': title, 'link': url, 'desc': desc})
            except Exception:
                urls.append({'title': title, 'link': url})
        print('Ask parsed: ' + str(urls))
        return urls

    @staticmethod
    def parse_video_response(soup):
        """ Parse response and returns the urls

            Returns: urls (list)
                    [[Tile1, url1], [Title2, url2], ...]
        """
        urls = []
        for div in soup.findAll('div', attrs={'class': 'v-info'}):
            title = div.div.find('a').getText()
            url = 'https' + div.div.a.get('href')
            desc = div.find('div', attrs={'class': 'desc'}).getText()
            urls.append({
                'title': title,
                'link': url,
                'desc': desc
            })

        print('Ask parsed: ' + str(urls))

        return urls
