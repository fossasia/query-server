from bs4 import BeautifulSoup

from app.scrapers import Parsijoo


def test_parse_response():
    html_text = """<div class="result">
    <span class="result-title">
    <a href="mock_url">""" + " " * 22 + """mock_title </a></span>
    <span class="result-url">mock_url</span>
    <span class="result-desc">""" + " " * 34 + """ mock_desc </span>
    <span class="result-similar"><a href="mock_similar_link"
    title="mock_similar_title">mock_similar</a>
    </span></div>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url',
        'desc': u'mock_desc'
    }]
    resp = Parsijoo().parse_response(dummy_soup)
    if not resp == expected_resp:
        raise AssertionError()
