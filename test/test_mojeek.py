from bs4 import BeautifulSoup

from app.scrapers import Mojeek


def test_parse_response():
    html_text = '<a href="mock_url" class="ob">mock_title</a>'
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Mojeek().parse_response(dummy_soup)
    assert resp == expected_resp
