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


def test_search_google_without_count():
    query = 'fossasia'
    expected_max_resp_count = 10
    resp_count = len(Google().search(query))
    assert resp_count <= expected_max_resp_count


def test_search_google_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(Google().search(query, 2))
    assert resp_count == expected_resp_count


def test_search_google_with_large_count():
    query = 'fossasia'
    expected_max_resp_count = 27
    resp_count = len(Google().search(query, 27))
    assert resp_count <= expected_max_resp_count
