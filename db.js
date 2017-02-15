var MongoClient = require('mongodb').MongoClient
var assert = require('assert');
var express = require('express');
var app = express();
var searcher = require(__dirname + '/search');


var url = 'mongodb://localhost:27017/query-server';

MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    console.log("Connected successfully to server");
    app.listen(7001);

    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    app.post('/',function(req, res, next) {
        searcher(req.query.search,displayResult);
        function displayResult( error, dataString){
          if(error)
              console.log(error);
          else
              console.log('****'+dataString+'*****');
        };
        //console.log(results);
        //res.send(results);
    });

    db.close();
});