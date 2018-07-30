import json

from mock import patch, MagicMock

from app.scrapers import Reddit


@patch('requests.models.Response')
@patch('app.scrapers.reddit.requests.get')
def test_search(mock_requests_get, mock_response):
    dummy_json = json.loads('''{
            "kind": "Listing",
            "data": {
                "children": [
                {
                    "data": {
                    "title": "queryserver",
                    "permalink": "/r/queryserver"
                    }
                }
                ],
                "before": null
            }
    }''')
    expected_resp = [
        {
            'text': u'queryserver',
            'link': u'https://www.reddit.com/r/queryserver'
        }
    ]
    mock_requests_get.return_value = mock_response
    mock_response.json = MagicMock(return_value=dummy_json)
    resp = Reddit().search('dummy_query', 1)
    assert expected_resp == resp
