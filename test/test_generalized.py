from mock import patch
import pytest

from app.scrapers.generalized import Scraper


@patch('requests.models.Response')
@patch('app.scrapers.generalized.requests.get')
def test_get_page(mock_request_get, mock_response):
    mock_request_get.return_value = mock_response
    mock_response.url = "Mock Url"
    response = Scraper().get_page("dummy_query")
    assert response == mock_response
    expected_payload = {'q': 'dummy_query', '': ''}
    expected_headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 '
            'Safari/537.36'
        )
    }
    mock_request_get.assert_called_with(
        '', headers=expected_headers, params=expected_payload)


def test_parse_response():
    with pytest.raises(NotImplementedError):
        Scraper().parse_response(None)


def test_next_start():
    dummy_prev_results = ['dummy_value']
    if not Scraper().next_start(3, dummy_prev_results) == 4:
        raise AssertionError()


@patch('app.scrapers.generalized.Scraper.parse_response')
@patch('app.scrapers.generalized.Scraper.get_page')
@patch('requests.models.Response')
def test_search(mock_resp, mock_get_page, mock_parse_resp):
    mock_get_page.return_value = mock_resp
    mock_resp.text = "Mock response"
    expected_resp = [{
        'title': 'mock_title',
        'link': 'mock_url'
    }]
    # assuming parse_response is being implemented by
    # classes inheriting Scraper. Thus, returning dummy
    # response instead of raising NotImplementedError
    mock_parse_resp.return_value = expected_resp
    resp = Scraper().search('dummy_query', 1)
    assert resp == expected_resp


@patch('app.scrapers.generalized.Scraper.get_page')
@patch('requests.models.Response')
def test_search_parsed_response_none(mock_resp, mock_get):
    mock_get.return_value = mock_resp
    mock_resp.text = "Mock Response"
    with patch('app.scrapers.generalized.Scraper.parse_response',
               return_value=None):
        resp = Scraper().search('dummy_query', 1)
        assert resp == []
