from bs4 import BeautifulSoup

from app.scrapers import Baidu


def test_parse_response():
    html_text = """<div class="result c-container "><h3 class="t">
        <a href="mock_url" target="_blank">mock_title</a>
        </h3></div>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Baidu().parse_response(dummy_soup)
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    assert resp == expected_resp


def test_search_baidu_without_count():
    query = 'fossasia'
    expected_max_resp_count = 10
    resp_count = len(Baidu().search(query))
    assert resp_count <= expected_max_resp_count


def test_search_baidu_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(Baidu().search(query, 2))
    assert resp_count == expected_resp_count


def test_search_baidu_with_large_count():
    query = 'fossasia'
    expected_max_resp_count = 27
    resp_count = len(Baidu().search(query, 27))
    assert resp_count <= expected_max_resp_count

def test_parse_news_response():
    html_text = """<h3 class="c-title">
        <a href="mock_url" target="_blank">mock_title</a>
        </h3>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Baidu().parse_news_response(dummy_soup)
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    assert resp == expected_resp
