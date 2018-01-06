import json
import os
from argparse import ArgumentParser
from defusedxml.minidom import parseString
from dicttoxml import dicttoxml
from flask import (Flask, Response, abort, jsonify, make_response,
                   render_template, request)
from pymongo import MongoClient
from scrapers import feed_gen, scrapers

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
    return render_template('index.html', engines_list=scrapers.keys())


def bad_request(error):
    message = {'Error': error[1], 'Status Code': error[0]}
    response = dicttoxml(message) if error[2] == 'xml' else json.dumps(message)
    return make_response(response, error[0])


@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    try:
        count = int(request.args.get('num', 10))
        qformat = request.args.get('format', 'json').lower()
        qtype = request.args.get('type','image').lower()
        if qformat not in ('json', 'xml', 'csv'):
            abort(400, 'Not Found - undefined format')
        
        if qtype not in ('image'):
            abort(400, 'Not Found - undefined query')

        engine = search_engine
        if engine not in scrapers:
            error = [404, 'Incorrect search engine', engine]
            return bad_request(error)

        query = request.args.get('query')
        if not query:
            error = [400, 'Not Found - missing query', qformat]
            return bad_request(error)
        # print("Extra query", qExtra)
        result = feed_gen(query, engine, count, qtype)
        print("Result", result)
        if not result:
            error = [404, 'No response', qformat]
            return bad_request(error)

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