from bs4 import BeautifulSoup

from app.scrapers import Google


def test_parse_response():
    html_text = """<h3 class="r">
    <a href="mock_url">mock_title</a>
    </h3>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Google().parse_response(dummy_soup)
    assert resp == expected_resp
