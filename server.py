from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
import requests
from pymongo import Connection

from rss_generator import passer
import json
from dicttoxml import dicttoxml
app=Flask(__name__)
@app.route('/')
def initial():
    
        return render_template('index.html',result=' ')
    
@app.route('/query', methods=['GET', 'POST'])
def query_processor():
        connection = Connection('localhost', 27017)
        db = connection['query_server']
        query=request.form['query']
        s_engine =request.form['s_engine'] 
        result= passer(query,s_engine)
        posts = db.posts
        datain=[]
        datain.append({'query': query,'result':result})
        posts.insert(datain)
        # print(result)
        # result = result.decode('utf-8')
        #tr=result.decode().strip('/n')
        # for m in tr:
        #     print(m)

        print(result)    
        return render_template('index.html',result=result)

@app.route('/api/v1/search', methods=['GET', 'POST'])
def querye():
    
    connection = Connection('localhost', 27017)
    db = connection['query-server']

    
    form='json'
    query = request.args.get('query')
    form = request.args.get('format')
    if(form=='json'):
        result= passer(query,'g')
        posts = db.result
        posts.insert(post)
        return json.dumps(result)
    else:
        result=passer(query,'g')
        posts = db.result
        posts.insert(post)
        xml = dicttoxml(result, custom_root='test', attr_type=False)
        print(xml)

        return xml


if __name__=='__main__':
    app.secret_key='super_secret_key'
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
