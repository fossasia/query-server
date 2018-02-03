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
    assert resp == expected_resp


def test_search_duckduckgo_without_count():
    query = 'fossasia'
    expected_max_resp_count = 10
    resp_count = len(DuckDuckGo().search(query))
    assert resp_count <= expected_max_resp_count


def test_search_duckduckgo_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(DuckDuckGo().search(query, 2))
    assert resp_count == expected_resp_count


def test_search_duckduckgo_with_large_count():
    query = 'fossasia'
    expected_max_resp_count = 27
    resp_count = len(DuckDuckGo().search(query, 27))
    assert resp_count <= expected_max_resp_count
