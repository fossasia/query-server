from flask import (Flask, Response, abort, make_response, render_template,
                   request)
from scrapers import get_scraper, feedgen
from pymongo import MongoClient
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import json
import os
from argparse import ArgumentParser

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
help = "Start the server in development mode with debug=True"
parser.add_argument("--dev", help=help, action="store_true")
args = parser.parse_args()


@app.route('/')
def index():
    return render_template('index.html')


def bad_request(err):
    message = {'Error': err[1], 'Status Code': err[0]}
    response = dicttoxml(message) if err[2] == 'xml' else json.dumps(message)
    return make_response(response, err[0])


@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    try:
        get_scraper(search_engine)
    except KeyError as e:
        print(e)
        err = [404, 'Incorrect search engine: ' + search_engine, search_engine]
        return bad_request(err)

    try:
        num = request.args.get('num', 10)
        count = int(num)
        qformat = request.args.get('format', 'json')
        if qformat not in ('json', 'xml'):
            abort(400, 'Not Found - undefined format')

        query = request.args.get('query')
        if not query:
            err = [400, 'Not Found - missing query', qformat]
            return bad_request(err)

        result = feedgen(query, search_engine, count)
        if not result:
            err = [404, 'No response', qformat]
            return bad_request(err)

        if db['queries'].find({query: query}).limit(1) is False:
            db['queries'].insert(
                {"query": query, "engine": search_engine, "qformat": qformat})

        for line in result:
            line['link'] = line['link'].encode('utf-8')
            line['title'] = line['title'].encode('utf-8')
            if 'desc' in line:
                line['desc'] = line['desc'].encode('utf-8')

        if qformat == 'json':
            jsonfeed = json.dumps(result).encode('utf-8')
            return Response(jsonfeed, mimetype='application/json')
        xmlfeed = parseString(
            (dicttoxml(
                result,
                custom_root='channel',
                attr_type=False))).toprettyxml()
        return Response(xmlfeed, mimetype='application/xml')
    except Exception as e:
        print(e)
        return Response(json.dumps(errorObj).encode(
            'utf-8'), mimetype='application/json')


@app.after_request
def set_header(r):
    r.headers["Cache-Control"] = "no-cache"
    return r


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7001))
    app.run(host='0.0.0.0', port=port, debug=args.dev)
