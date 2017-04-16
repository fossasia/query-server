from flask import Flask, render_template, request, url_for, abort
from scraper import feedgen
from pymongo import MongoClient
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import json,os 

app = Flask(__name__)

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['query-server-v2']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/search/<search_engine>', methods=['GET'])
def search(search_engine):
    try:
        if request.method == 'GET':

            engine = search_engine
            if engine not in ['google','bing','duckduckgo','yahoo']:
                abort(404)

            query = request.args.get('query')
            if not query:
                abort(400)

            qformat = request.args.get('format') or 'json'
            if qformat not in ['json','xml']:
                abort(400)

            result = feedgen(query,engine[0])
            if not result:
                abort(404)

            if((db['queries'].find({query: query}).limit(1)) == False):
                db['queries'].insert({"query" : query,  "engine" : engine, "qformat" : qformat})

            for line in result:
                line['link'] = line['link'].encode('utf-8')
                line['title'] = line['title'].encode('utf-8')
                if( engine == 'b'):
                    line['desc'] = line['desc'].encode('utf-8')

            if(qformat == 'json'):
                jsonfeed = json.dumps(result, indent=4).encode('utf-8')
                return jsonfeed

            elif(qformat == 'xml'):
                xmlfeed = parseString((dicttoxml(result, custom_root='channel', attr_type=False)).encode('utf-8')).toprettyxml()
                return xmlfeed

    except Exception as e:
        return (e)
      
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=(int)(os.environ.get('PORT', 7001)), debug=True)