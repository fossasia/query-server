import json
import os

import pytest
import requests
from defusedxml import ElementTree
from mock import patch

from app.scrapers import small_test
from app.server import app

REASON = 'Do you have query-server running on http://127.0.0.1:7001 ?'
TRAVIS_CI = os.getenv('TRAVIS', False)  # Running in Travis CI?


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_small_test():
    small_test()


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_invalid_url_api_call():
    response = requests.get('http://localhost:7001/api/v1/search/invalid_url')
    if not response.json()['Status Code'] == 404:
        raise AssertionError()


def make_engine_api_call(engine_name):
    url = 'http://localhost:7001/api/v1/search/' + engine_name
    if requests.get(url).json()['Status Code'] != 400:
        raise AssertionError()


@pytest.mark.xfail(not TRAVIS_CI, reason=REASON)
def test_engine_api_calls(engine_names=None):
    engines = """ask baidu bing dailymotion duckduckgo exalead google
                 mojeek parsijoo quora yahoo yandex youtube""".split()
    for engine_name in (engine_names or engines):
        make_engine_api_call(engine_name)


def test_api_index():
    if not app.test_client().get('/').status_code == 200:
        raise AssertionError()


@patch('app.server.abort')
def test_api_search_invalid_qformat(mock_abort):
    url = '/api/v1/search/google?query=fossasia&format=invalid'
    app.test_client().get(url)
    mock_abort.assert_called_with(400, 'Not Found - undefined format')


@patch('app.server.bad_request', return_value="Mock Response")
def test_api_search_invalid_engine(mock_bad_request):
    url = '/api/v1/search/invalid?query=fossasia'
    resp = app.test_client().get(url).get_data().decode('utf-8')
    mock_bad_request.assert_called_with(
        [404, 'Incorrect search engine', 'invalid'])
    if not resp == "Mock Response":
        raise AssertionError()


@patch('app.server.bad_request', return_value="Mock Response")
def test_api_search_missing_query(mock_bad_request):
    # invalid url with query parameter missing
    url = '/api/v1/search/google'
    resp = app.test_client().get(url).get_data().decode('utf-8')
    mock_bad_request.assert_called_with(
        [400, 'Not Found - missing query', 'json'])
    if not resp == "Mock Response":
        raise AssertionError()


@patch('app.server.bad_request', return_value="Mock Response")
def test_api_search_for_no_response(mock_bad_request):
    url = '/api/v1/search/google?query=fossasia'
    with patch('app.server.lookup', return_value=None):
        with patch('app.server.feed_gen', return_value=None):
            resp = app.test_client().get(url).get_data().decode('utf-8')
            mock_bad_request.assert_called_with([404, 'No response',
                                                 'google:fossasia'])
            if not resp == "Mock Response":
                raise AssertionError()


def test_api_search_for_cache_hit():
    url = '/api/v1/search/google?query=fossasia'
    mock_result = [{'title': 'mock_title', 'link': 'mock_link'}]
    with patch('app.server.lookup', return_value=mock_result):
        resp = app.test_client().get(url).get_data().decode('utf-8')
        if not json.loads(resp) == mock_result:
            raise AssertionError()


@patch('app.server.feed_gen')
@patch('app.server.lookup')
def test_api_search_for_format(mock_lookup, mock_feed_gen):
    for qformat in ['json', 'csv', 'xml']:
        url = '/api/v1/search/google?query=fossasia&format=' + qformat
        mock_result = [
            {
                'title': 'mock_title',
                'link': 'mock_link',
                'desc': 'mock_desc'
            }
        ]
        mock_lookup.return_value = None
        mock_feed_gen.return_value = mock_result
        resp = app.test_client().get(url).get_data().decode('utf-8')
        expected_resp = expected_response_for_format(qformat)
        if qformat == 'json':
            resp = json.loads(resp)
        elif qformat == 'xml':
            resp = resp.replace('\t', '').replace('\n', '')
            resp = get_json_equivalent_from_xml_feed(resp)
            expected_resp = get_json_equivalent_from_xml_feed(expected_resp)
        elif qformat == 'csv':
            resp = get_json_equivalent_from_csv_feed(resp)
            expected_resp = get_json_equivalent_from_csv_feed(expected_resp)
        if not expected_resp == resp:
            raise AssertionError()


def expected_response_for_format(qformat):
    if qformat == 'json':
        return [
            {'title': 'mock_title',
             'link': 'mock_link',
             'desc': 'mock_desc'}
        ]
    elif qformat == 'csv':
        return '"link","title","desc"\n"mock_link","mock_title","mock_desc"'
    elif qformat == 'xml':
        return '<?xml version="1.0" ?><channel><item>' \
               '<desc>mock_desc</desc><link>mock_link</link>' \
               '<title>mock_title</title></item></channel>'


def get_json_equivalent_from_csv_feed(feed):
    keys_feed1 = feed.split('\n')[0].split(',')
    json_result = []
    for row_index, row in enumerate(feed.split('\n')):
        if row_index == 0:
            continue
        entry = {}
        for index, value in enumerate(row.split(',')):
            entry[keys_feed1[index].replace('"', '')] = value.replace('"', '')
        json_result.append(entry)
    return json_result


def get_json_equivalent_from_xml_feed(feed):
    def internal_iter(tree, accum):
        if tree is None:
            return accum

        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text

        return accum

    return internal_iter(ElementTree.fromstring(feed), {})
