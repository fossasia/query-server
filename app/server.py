import os
from argparse import ArgumentParser

from defusedxml.minidom import parseString
from dicttoxml import dicttoxml
from flask import (Flask, Response, abort, jsonify,
                   render_template, request)

try:
    from scrapers import feed_gen, scrapers
except Exception as e:
    from app.scrapers import feed_gen, scrapers

DISABLE_CACHE = True  # Temporarily disable the MongoDB cache
if DISABLE_CACHE:
    def lookup(url):
        return False

    def store(url, links):
        pass
else:
    from query_cache import lookup, store

app = Flask(__name__)
err = ""

errorObj = {
    'type': 'Internal Server Error',
    'status_code': 500,
    'error': 'Could not parse the page due to Internal Server Error'
}


@app.route('/')
def index():
    return render_template('index.html', engines_list=scrapers.keys())


def bad_request(error):
    message = {'Error': error[1], 'Status Code': error[0]}
    print(error[2])
    if error[2] == 'xml':
        return Response(dicttoxml(message), mimetype='text/xml')
    elif error[2] == 'csv':
        message = "'Error', 'Status Code' \n {}, {}".format(error[1], error[0])
        return Response(message, mimetype='text/csv')
    else:
        return jsonify(message)


@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    try:
        count = int(request.args.get('num', 10))
        qformat = request.args.get('format', 'json').lower()
        qtype = request.args.get('type', '')
        if qformat not in ('json', 'xml', 'csv'):
            abort(400, 'Not Found - undefined format')

        engine = search_engine
        if engine not in scrapers:
            error = [404, 'Incorrect search engine', engine]
            return bad_request(error)

        query = request.args.get('query')
        if not query:
            error = [400, 'Not Found - missing query', qformat]
            return bad_request(error)

        # first see if we can get the results for the cache
        engine_and_query = engine + ':' + query
        result = lookup(engine_and_query)
        if result:
            print("cache hit: {}".format(engine_and_query))
        else:
            result, status_code = feed_gen(query, engine, count, qtype)
            if result:
                # store the result in the cache to speed up future searches
                store(engine_and_query, result)
            else:
                error = [status_code, 'No response', engine_and_query]
                return bad_request(error)

        try:
            unicode  # unicode is undefined in Python 3 so NameError is raised
            for line in result:
                line['link'] = line['link'].encode('utf-8')
                if 'title' in line:
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
    parser = ArgumentParser()
    help_msg = "Start the server in development mode with debug=True"
    parser.add_argument("--dev", help=help_msg, action="store_true")
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=port, debug=args.dev)
