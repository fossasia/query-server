import json
import os
from dicttoxml import dicttoxml
from flask import (Flask, render_template, request, abort, Response,
                   make_response)
from pymongo import MongoClient
from xml.dom.minidom import parseString
from scrapers import feedgen


app = Flask(__name__)
err = ""

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['query-server-v2']
errorObj = {
    'type': 'Internal Server Error',
    'status_code': 500,
    'error': 'Could not parse the page due to Internal Server Error'
}


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
        count = int(request.args.get('num') or 10)
        qformat = request.args.get('format', 'json')
        if qformat not in ('json', 'xml'):
            abort(400, 'Not Found - undefined format')
        query = request.args.get('query')
        if not query:
            return bad_request([400, 'Not Found - missing query', qformat])
        try:
            result = feedgen(query, search_engine, count)
        except KeyError:
            return bad_request([404, 'Incorrect search engine', qformat])
        if not result:
            return bad_request([404, 'No response', qformat])

        if db['queries'].find({query: query}).limit(1) is False:
            db['queries'].insert(
                {"query": query, "engine": search_engine, "qformat": qformat})

        for line in result:
            for key, value in line.items():
                line[key] = value.encode('utf-8')
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
    app.run(
        host='0.0.0.0',
        port=int(
            os.environ.get(
                'PORT',
                7001)),
        debug=True)
