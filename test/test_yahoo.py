from bs4 import BeautifulSoup

from app.scrapers import Yahoo


def test_parse_response():
    html_text = '<h3 class="title"><a class=" ac-algo fz-l ac-21th lh-24"' \
        ' href="//r.search.yahoo.com/_ylt=Awr;_ylu=X3--/RV=2/RE=15/RO=10' \
        '/RU=mock_url/RK=2/RS=Gne">mock_title</a></h3> '
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Yahoo().parse_response(dummy_soup)
    assert resp == expected_resp


def test_parse_image_response():
    html_text = """<li class="ld"><a aria-label="mock_title">
                <img data-src='mock_url' class='process'/></a></div>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Yahoo().parse_image_response(dummy_soup)
    assert resp == expected_resp
