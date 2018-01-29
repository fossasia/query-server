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
    assert resp == expected_resp


def test_parse_video_response():
    html_text = """<a href="mock_url" class="over-page"
    title="mock_title">mock_title</a>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    url = 'https://video.parsijoo.ir' + "mock_url"
    expected_resp = [{
        'title': u'mock_title',
        'link': url,
    }]
    resp = Parsijoo().parse_video_response(dummy_soup)
    assert resp == expected_resp


def test_parse_image_response():
    html_text = """<div class="image-container overflow"><a href="mock_url"
    title="mock_title">mock_title</a></div>"""
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    image_url = 'https://image.parsijoo.ir' + 'mock_url'
    expected_resp = [{
        'link': image_url,
    }]
    resp = Parsijoo().parse_image_response(dummy_soup)
    assert resp == expected_resp
