var express = require('express');
var app = express();
var searcher = require(__dirname + '/search');

app.listen(7001);

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.post('/',function(req, res, next) {
    //console.log(req.query.search);
    results = searcher(req.query.search);
    console.log(results);
    res.send(results);
});
