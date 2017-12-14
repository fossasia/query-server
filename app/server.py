#!/usr/bin/env python3
import json
import os
from argparse import ArgumentParser

from defusedxml.minidom import parseString
from dicttoxml import dicttoxml
from flask import (Flask, Response, jsonify, make_response,
                   render_template, request)
from pymongo import MongoClient

from scrapers.scraper import get_scrapers

app = Flask(__name__)
err = ""

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['query-server-v2']
errorObj = {
    'type': 'Internal Server Error',
    'status_code': 500,
    'error': 'Could not parse the page due to Internal Server Error'
}

parser = ArgumentParser()
help_msg = "Start the server in development mode with debug=True"
parser.add_argument("--dev", help=help_msg, action="store_true")
args = parser.parse_args()

search_engines = ["google", "yahoo", "bing", "ask", "duckduckgo", "yandex",
                  "youtube", "exalead", "mojeek", "dailymotion", "parsijoo",
                  "quora", "baidu"]


@app.route('/')
def index():
    return render_template('index.html', engines_list=search_engines)


def bad_request(error):
    message = {'Error': error[1], 'Status Code': error[0]}
    response = dicttoxml(message) if error[2] == 'xml' else json.dumps(message)
    return make_response(response, error[0])


@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    print(search_engine)
    # convert search_engine into engine which should be a Scraper class
    try:
        engine = get_scrapers()[search_engine.lower()]
    except KeyError:
        err = [404, 'Incorrect search engine', search_engine]
        return bad_request(err)

    # get the query parameter
    query = request.args.get('query')
    if not query:
        err = [400, 'Not Found - missing query', query]
        return bad_request(err)

    # get the output format parameter
    qformat = request.args.get('format', 'json').lower()
    if qformat not in ('json', 'xml'):
        err = [400, 'Not Found - undefined format', qformat]
        return bad_request(err)
    print(qformat)
    # get the num parameter
    num = request.args.get('num', 10)
    try:
        num = int(num)
    except (TypeError, ValueError):
        err = [400, 'Not Found - invalid num parameter', num]
        return bad_request(err)
    print(num)

    # we should now have valid search_engine, query, output format, and num...
    result = engine().search(query, num)
    if not result:
        err = [404, 'No response', qformat]
        return bad_request(err)

    try:
        if db['queries'].find({query: query}).limit(1) is False:
            db['queries'].insert({
                "query": query,
                "engine": engine,
                "qformat": qformat
            })

        try:
            unicode  # unicode is undefined in Python 3 so NameError is raised
            for line in result:
                line['link'] = line['link'].encode('utf-8')
                line['title'] = line['title'].encode('utf-8')
                if 'desc' in line:
                    line['desc'] = line['desc'].encode('utf-8')
        except NameError:
            pass  # Python 3 strings are already Unicode

        if qformat == 'json':
            return jsonify(result)
        elif qformat == 'csv':
            csvfeed = '"'
            csvfeed += '","'.join(result[0].keys())
            for line in result:
                csvfeed += '"\n"'
                csvfeed += '","'.join(line.values())
            csvfeed += '"'
            return Response(csvfeed)

        xmlfeed = dicttoxml(result, custom_root='channel', attr_type=False)
        xmlfeed = parseString(xmlfeed).toprettyxml()
        return Response(xmlfeed, mimetype='application/xml')
    except Exception as e:
        print(e)
        return jsonify(errorObj)


@app.after_request
def set_header(r):
    r.headers["Cache-Control"] = "no-cache"
    return r


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7001))
    app.run(host='0.0.0.0', port=port, debug=args.dev)
