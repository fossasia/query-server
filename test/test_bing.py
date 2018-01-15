from bs4 import BeautifulSoup

from app.scrapers import Bing


def test_parse_response():
    html_text = """<li class="b_algo">
        <h2><a href="mock_url">mock_title</h2>
        <div class="b_caption"><p>mock_desc</p>
        </div><li>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Bing().parse_response(dummy_soup)
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url',
        'desc': u'mock_desc'
    }]
    if not expected_resp == resp:
        raise AssertionError()
