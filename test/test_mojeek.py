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


def test_search_mojeek_without_count():
    query = 'fossasia'
    expected_max_resp_count = 10
    resp_count = len(Mojeek().search(query))
    assert resp_count == expected_max_resp_count


def test_search_mojeek_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(Mojeek().search(query, 2))
    assert resp_count == expected_resp_count


def test_search_mojeek_with_large_count():
    query = 'fossasia'
    expected_max_resp_count = 27
    resp_count = len(Mojeek().search(query, 27))
    assert resp_count == expected_max_resp_count


def test_parse_news_response():
    html_text = '<a href="mock_url" class="ob">mock_title</a>'
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Mojeek().parse_news_response(dummy_soup)
    assert resp == expected_resp
