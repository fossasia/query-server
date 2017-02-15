var path = require('path');
var fs = require('fs');
var util = require('util');
var spawn = require('child_process').spawn;

var query = '';
var dataString = "";

var queries = fs.readFileSync('data/query_list.txt').toString().split("\n");
var search = function(data) {
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
            var xml_file = __dirname + 'data/' + myquery + '.xml';
            console.log(' saved to file : ' + xml_file);
            return xml_file;
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
};
module.exports = search ;
