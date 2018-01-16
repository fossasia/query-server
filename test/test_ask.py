from bs4 import BeautifulSoup

from app.scrapers import Ask


def test_next_start():
    assert 3 == Ask().next_start(2, None)


def test_parse_response_for_none():
    html_text = """<div class="PartialSearchResults-noresults">
         <div class="PartialSearchResults-noresults-body">
             <p>No results for:</p>
             <p><b>44754546546545545465465f4654f654654</b></p>
             <p>Please try again.</p>
         </div>
    </div>"""
    stub_soup = BeautifulSoup(html_text, 'html.parser')
    resp = Ask().parse_response(stub_soup)
    assert resp is None


def test_parse_response_with_desc():
    html_div = """<div class="PartialSearchResults-item" data-zen="true">
        <div class="PartialSearchResults-item-title">
            <a class="PartialSearchResults-item-title-link result-link"
             href='mock_url'>mock_title</a>
        </div>
        <p class="PartialSearchResults-item-abstract">mock_desc</p>
        </div>"""
    stub_soup_div = BeautifulSoup(html_div, 'html.parser')
    resp = Ask().parse_response(stub_soup_div)
    expected_resp = [
        {
            'link': u'mock_url',
            'title': u'mock_title',
            'desc': u'mock_desc'
        }
    ]
    assert resp == expected_resp


def test_parse_response_without_desc():
    html_div = """<div class="PartialSearchResults-item" data-zen="true">
        <div class="PartialSearchResults-item-title">
            <a class="PartialSearchResults-item-title-link result-link"
             href='mock_url'>mock_title</a>
        </div>
        </div>"""
    stub_soup_div = BeautifulSoup(html_div, 'html.parser')
    resp = Ask().parse_response(stub_soup_div)
    expected_resp = [
        {
            'link': u'mock_url',
            'title': u'mock_title'
        }
    ]
    assert resp == expected_resp
