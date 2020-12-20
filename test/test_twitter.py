import json

from unittest.mock import patch, MagicMock

from app.scrapers import Twitter


@patch('requests.models.Response')
@patch('app.scrapers.twitter.requests.get')
def test_search(mock_requests_get, mock_response):
    dummy_json = json.loads('''{
      "aggregations": {},
      "readme_3": "mock_data",
      "statuses": [
        {
          "hosts_count": 1,
          "links": [
            "http://Phimp.Me"
          ],
          "text": "mock_text",
          "retweet_count": 0,
          "source_type": "TWITTER",
          "link": "mock_link",
          "links_count": 1
        }
      ]
    }''')
    expected_resp = [
        {
            'text': u'mock_text',
            'link': u'mock_link'
        }
    ]
    mock_requests_get.return_value = mock_response
    mock_response.json = MagicMock(return_value=dummy_json)
    resp = Twitter().search('dummy_query', 1)
    assert expected_resp == resp
