from bs4 import BeautifulSoup

from app.scrapers import DuckDuckGo


def test_parse_response():
    html_text = """<h2 class="result__title">
        <a class="result__a" href="mock_url">mock_title</a>
        </h2>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    resp = DuckDuckGo().parse_response(dummy_soup)
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    if not resp == expected_resp:
        raise AssertionError()
