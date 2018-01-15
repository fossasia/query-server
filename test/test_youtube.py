from bs4 import BeautifulSoup

from app.scrapers import Youtube


def test_parse_response():
    html_text = '<a href="/channel/UCQprMsG-raCIMlBudm20iLQ" ' \
        'class="yt-uix-sessionlink">mock_channel</a><a href=' \
        '"/watch?v=mock" class="yt-uix-tile-link yt-ui-ellipsis ' \
        'yt-ui-ellipsis-2 yt-uix-sessionlink" ' \
        'title="mock_title">mock_title</a>'
    dummy_soup = BeautifulSoup(html_text, 'html.parser')
    expected_resp = [{
        'title': u'mock_title',
        'link': u'https://www.youtube.com/watch?v=mock'
    }]
    resp = Youtube().parse_response(dummy_soup)
    if not resp == expected_resp:
        raise AssertionError()
