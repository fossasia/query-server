from bs4 import BeautifulSoup

from app.scrapers import Quora


def test_parse_response():
    html_text = ("<div><a class='question_link' href='/mock_url'>"
                 "<span class='question_text'><span class='rendered_qtext'>"
                 "mock_title</span></span></a></div>")
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'https://www.quora.com/mock_url'
    }]
    resp = Quora().parse_response(dummy_soup)
    assert resp == expected_resp


# Quora search for "fossasia" returns 9 results
def test_search_quora_without_count():
    query = 'fossasia'
    actual_resp_count = 9
    expected_max_resp_count = 10
    resp_count = len(Quora().search(query))
    assert (resp_count == actual_resp_count) and \
           (resp_count <= expected_max_resp_count)


def test_search_quora_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(Quora().search(query, 2))
    assert resp_count == expected_resp_count


# Quora search for "fossasia" returns 9 results
def test_search_quora_with_large_count():
    query = 'fossasia'
    actual_resp_count = 9
    expected_max_resp_count = 27
    resp_count = len(Quora().search(query, 27))
    assert (resp_count == actual_resp_count) and \
           (resp_count <= expected_max_resp_count)
