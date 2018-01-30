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
