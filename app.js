var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var express = require('express');
var app = express();
var searcher = require(__dirname + '/search');
var path = require('path');
var fs = require('fs');
var util = require('util');
var ejs = require('ejs');
var favicon = require('serve-favicon');
var spawn = require('child_process').spawn;
var url = process.env.MONGODB_URI;

MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    console.log("Connected successfully to server");

    app.listen(process.env.PORT || 7001);
    app.use(express.static(path.join(__dirname)));
    app.set('view engine', 'ejs');
    app.set('views', path.join(__dirname, 'views'));
    app.use(favicon(path.join(__dirname,'public','images','favicon.ico')));

    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    app.post('/submit',function(req, res, next) {
        var data = req.query.search;
        var myquery = data.toString();
        db.collection('xml_files').find({'query': myquery}).count()
            .then(function(numItems) {
                var query_raw = myquery;
                myquery = myquery.split('~')[1];
                if (numItems == 0  ) {
                    dataString = '';
                    console.log("        querying -> " + myquery);

                    var py = spawn('python', ['rss-generator.py']);

                    py.stdout.on('data', function (data) {
                        dataString += data.toString();
                    });

                    py.stdout.on('end', function () {
                        console.log(dataString);
                        var dbObject = {query: query_raw, xml: dataString};
                        db.collection('xml_files').save(dbObject, function (err, result) {
                            if (err) return console.log(err);
                            console.log('saved to database');
                            rval(query_raw);
                        });
                    });

                    py.stdin.write(JSON.stringify(data));
                    py.stdin.end();

                } else {
                    console.log(" already queried -> " + myquery);
                    rval(query_raw);
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