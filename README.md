# Query-Server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)
[![Dependency Status](https://david-dm.org/fossasia/query-server.svg)](https://david-dm.org/ossasia/query-server)
[![Join the chat at https://gitter.im/fossasia/query-server](https://badges.gitter.im/fossasia/query-server.svg)](https://gitter.im/fossasia/query-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

> The query server can be used to search a keyword/phrase on a search engine (Google, Yahoo, Bing, DuckDuckGo) and get the results as `json` or `xml`. The tool also stores the searched query string in a MongoDB database for analytical purposes. (The search engine scrapper is based on the scraper at [fossasia/searss](https://github.com/fossasia/searss).)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/fossasia/query-server)

## Table of Contents

- [API](#api)
- [Error Codes](#error-codes)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contribute](#contribute)

## API

The API(s) provided by query-server are as follows:

` GET /api/v1/search/<search-engine>?query=query&format=format `

> *search-engine* : ['google' , 'bing', 'duckduckgo' , 'yahoo']

> *query* : query can be any string 

> *format* : [ `json`, `xml` ]

A sample query : `/api/v1/search/bing?query=fossasia&format=xml&num=10`

## Error Codes
    404 Not Found : Incorrect Search Engine, Zero Response
    400 Bad Request : query and/or format is not in the correct format
    500 Internal Server Error : Server Error from Search Engine

## Dependencies

* [MongoDB](https://www.mongodb.com)
* [Python 2.7 and 3.4+](https://python.org) `  ` Best practice: [__pip install -r requirements.txt__](requirements.txt)
    * [Pip](https://pip.pypa.io/en/stable/installing)
    * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc)
    * [dicttoxml](https://github.com/quandyfactory/dicttoxml)
    * [Flask](http://flask.pocoo.org)
    * [pymongo](https://api.mongodb.com/python/current)
    * [requests](http://docs.python-requests.org)
* [Node.js](https://nodejs.org/en)
    * [bower.io](https://bower.io)

## Installation

Make sure you have [Nodejs](https://nodejs.org/en/) installed.
Running this tool requires installing the nodejs as well as python dependencies.

```
git clone https://github.com/fossasia/query-server.git 
cd query-server
npm install -g bower
bower install
pip install -r requirements.txt
```

To set up MongoDB on your server : 
```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start
```

## Usage

To run the query server: 
```bash
python app/server.py
```

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/fossasia/query-server/issues)

## License

This project is currently licensed under the Apache License version 2.0. A copy of `LICENSE` should be present along with the source code. To obtain the software under a different license, please contact [FOSSASIA](http://blog.fossasia.org/contact/).

