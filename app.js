var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var express = require('express');
var app = express();
var searcher = require(__dirname + '/search');
var path = require('path');
var fs = require('fs');
var util = require('util');
var ejs = require('ejs');
var spawn = require('child_process').spawn;

var url = 'mongodb://localhost:27017/query-server';

MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    console.log("Connected successfully to server");

    app.listen(7001);
    app.use(express.static(path.join(__dirname)));
    app.set('view engine', 'ejs');
    app.set('views', path.join(__dirname, 'views'));

    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    app.post('/submit',function(req, res, next) {
        var data = req.query.search;
        var myquery = data.toString();
        myquery = myquery.split('~')[1];
        db.collection('xml_files').find({'query': myquery}).count()
            .then(function(numItems) {
                if (numItems == 0  ) {
                    dataString = '';
                    console.log("        querying -> " + myquery);

                    var py = spawn('python', ['rss-generator.py']);

                    py.stdout.on('data', function (data) {
                        dataString += data.toString();
                    });

                    py.stdout.on('end', function () {
                        console.log(dataString);
                        var dbObject = {query: myquery, xml: dataString};
                        db.collection('xml_files').save(dbObject, function (err, result) {
                            if (err) return console.log(err);
                            console.log('saved to database');
                            rval(myquery);
                        });
                    });

                    py.stdin.write(JSON.stringify(data));
                    py.stdin.end();

                } else {
                    console.log(" already queried -> " + myquery);
                    rval(myquery);
                }
            });
        var rval = function(myquery) {
            db.collection('xml_files').find({"query": myquery}).toArray(function (err, results) {
                if (err) return console.log(err);
                res.render('index', {dbObject: results});
            });
        };
    });
});