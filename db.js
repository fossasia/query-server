var MongoClient = require('mongodb').MongoClient
var assert = require('assert');
var express = require('express');
var app = express();
var searcher = require(__dirname + '/search');
var path = require('path');
var fs = require('fs');
var util = require('util');
var spawn = require('child_process').spawn;

var query = '';
var dataString = "";
var queries = [];
var url = 'mongodb://localhost:27017/query-server';

MongoClient.connect(url, function(err, db) {
    assert.equal(null, err);
    console.log("Connected successfully to server");
    app.listen(7001);

    app.get('/', function(req, res) {
        res.sendFile(__dirname + '/index.html');
    });

    app.post('/',function(req, res, next) {
        var data = req.query.search;
        //console.log(results);
        //var search = function(data) {
        //console.log(data);
        if (queries.indexOf(data) == -1) {
            dataString = '';
            queries.push(data);
            var myquery = data.toString();
            myquery = myquery.split('~')[1];
            console.log("        querying -> " + myquery);
            var py = spawn('python', ['rss-generator.py']);

            py.stdout.on('data', function(data) {
                dataString += data.toString();
            });

            py.stdout.on('end', function() {
                console.log(dataString);
                var xml_file = __dirname + '/data/' + myquery + '.xml';
                console.log(' saved to file : ' + xml_file);
                var dbObject =  { query : myquery , xml : dataString , file : xml_file } ;
                db.collection('xml_files').save(dbObject, function(err, result){
                    if (err) return console.log(err);
                    console.log('saved to database');
                    res.redirect('/')
                });
            });

            py.stdin.write(JSON.stringify(data));
            py.stdin.end();

            fs.appendFile('data/query_list.txt', queries[queries.length-1] + '\n', function(err) {
                if (err) console.log(err);
            });
        } else {
            var myquery = data.toString();
            console.log(" already queried -> " + myquery);
            console.log(' saved to file : query-server/data/' + myquery + '.xml');

        }
    });
    //db.close();
});