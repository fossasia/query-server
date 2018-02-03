from bs4 import BeautifulSoup

from app.scrapers import Yahoo


def test_parse_response():
    html_text = ('<h3 class="title"><a class=" ac-algo fz-l ac-21th lh-24" '
                 'href="//r.search.yahoo.com/_ylt=Awr;_ylu=X3--/RV=2/RE=15/'
                 'RO=10/RU=mock_url/RK=2/RS=Gne">mock_title</a></h3> ')
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url'
    }]
    resp = Yahoo().parse_response(dummy_soup)
    assert resp == expected_resp


def test_search_yahoo_without_count():
    query = 'fossasia'
    expected_max_resp_count = 10
    resp_count = len(Yahoo().search(query))
    assert resp_count <= expected_max_resp_count


def test_search_yahoo_with_small_count():
    query = 'fossasia'
    expected_resp_count = 2
    resp_count = len(Yahoo().search(query, 2))
    assert resp_count == expected_resp_count


def test_search_yahoo_with_large_count():
    query = 'fossasia'
    expected_max_resp_count = 27
    resp_count = len(Yahoo().search(query, 27))
    assert resp_count <= expected_max_resp_count


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


def test_parse_news_response():
    html_text = '<div class="dd algo NewsArticle"><div class="layoutLeft">' \
        '<div class="compTitle"><h3><a class="fz-m" href="http://' \
        'r.search.yahoo.com/_ylt=Awr;_ylu=X3--/RV=2/RE=15/RO=10/RU=mock_url/' \
        'RK=2/RS=Gne">mock_title</a></h3><div class="compText" ><p>mock_desc'\
        '</p></div></div>'
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'mock_url',
        'desc': u'mock_desc'
    }]
    resp = Yahoo().parse_news_response(dummy_soup)
    assert resp == expected_resp
