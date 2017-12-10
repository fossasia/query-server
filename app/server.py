import json
import os
from argparse import ArgumentParser
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flask import (Flask, Response, abort, jsonify, make_response,
                   render_template, request)
from pymongo import MongoClient

from scrapers import feedgen, scrapers

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
        count = int(request.args.get('num', 10))
        qformat = request.args.get('format', 'json').lower()
        if qformat not in ('json', 'xml'):
            abort(400, 'Not Found - undefined format')

        engine = search_engine
        if engine not in scrapers:
            err = [404, 'Incorrect search engine', engine]
            return bad_request(err)

        query = request.args.get('query')
        if not query:
            err = [400, 'Not Found - missing query', qformat]
            return bad_request(err)

        result = feedgen(query, engine, count)
        if not result:
            err = [404, 'No response', qformat]
            return bad_request(err)

        if db['queries'].find({query: query}).limit(1) is False:
            db['queries'].insert(
                {"query": query, "engine": engine, "qformat": qformat})

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
