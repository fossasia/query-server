from flask import Flask, render_template, request, url_for, abort, Response, make_response
from scrapers import feedgen
from pymongo import MongoClient
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import json,os

app = Flask(__name__)
err = ""

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['query-server-v2']

@app.route('/')
def index():
    return render_template('index.html')

def bad_request(err):
    message = {'Error': err[1], 'Status Code': err[0]}
    if(err[2] == 'xml'):
        response = dicttoxml(message)
    else:
        response = json.dumps(message)
    resp = make_response(response, err[0])
    return resp

@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    try:
        if request.method == 'GET':

            qformat = request.args.get('format') or 'json'
            if qformat not in ['json', 'xml']:
                abort(400, 'Not Found - undefined format')

            engine = search_engine
            if engine not in ['google','bing','duckduckgo','yahoo']:
                err = [404, 'Incorrect search engine', qformat]
                return bad_request(err)

            query = request.args.get('query')
            if not query:
                err = [400, 'Not Found - missing query', qformat]
                return bad_request(err)

            result = feedgen(query,engine[0])
            if not result:
                err = [404, 'No response', qformat]
                return bad_request(err)

            if((db['queries'].find({query: query}).limit(1)) == False):
                db['queries'].insert({"query" : query,  "engine" : engine, "qformat" : qformat})

            for line in result:
                line['link'] = line['link'].encode('utf-8')
                line['title'] = line['title'].encode('utf-8')
                if( engine == 'b'):
                    line['desc'] = line['desc'].encode('utf-8')

            if(qformat == 'json'):
                jsonfeed = json.dumps(result).encode('utf-8')
                return Response(jsonfeed, mimetype='application/json')

            elif(qformat == 'xml'):
                xmlfeed = parseString((dicttoxml(result, custom_root='channel', attr_type=False)).encode('utf-8')).toprettyxml()
                return Response(xmlfeed, mimetype='application/xml')

    except Exception as e:
        return (e)

@app.after_request
def set_header(r):
    r.headers["Cache-Control"] = "no-cache"
    return r

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=(int)(os.environ.get('PORT', 7001)), debug=True)