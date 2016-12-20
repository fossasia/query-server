var express = require('express');
var path = require('path');
var fs = require('fs');
var util = require('util');
var spawn = require('child_process').spawn;
var readline = require('readline');

var query = '';
var dataString = "";

var queries = fs.readFileSync('data/query_list.txt').toString().split("\n");
var rl = readline.createInterface(process.stdin, process.stdout);

rl.setPrompt('\nSearch for >> ');
rl.prompt();
rl.on('line', function(line) {
    data = line;
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
            console.log(" saved to file : " + __dirname + '/data/' + myquery + '.xml');
            rl.prompt();
        });

        py.stdin.write(JSON.stringify(data));
        py.stdin.end();

        queries.forEach(function(v) {
            fs.appendFile('data/query_list.txt', v + '\n', function(err) {
                if (err) console.log(err);
            });
        });
    } else {
        console.log(" already queried -> " + myquery);
        console.log(" saved to file : " + __dirname + '/data/' + myquery + '.xml');
        rl.prompt();
    }
});