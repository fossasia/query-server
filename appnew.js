var express = require('express');
var fs = require('fs');
var path = require('path');
var app = express();
app.use(express.static(path.join(__dirname, 'public')));
var searcher = require(__dirname + '/search');

app.listen(7001);

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.post('/',function(req, res, next) {
    console.log(req.query.search);
    results = searcher(req.query.search);
    console.log(results);
    res.send(results);
});
