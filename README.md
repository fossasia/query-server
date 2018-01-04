# Query-Server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)
[![Dependency Status](https://david-dm.org/fossasia/query-server.svg)](https://david-dm.org/ossasia/query-server)
[![Join the chat at https://gitter.im/fossasia/query-server](https://badges.gitter.im/fossasia/query-server.svg)](https://gitter.im/fossasia/query-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

> The query server can be used to search a keyword/phrase on a search engine (Google, Yahoo, Bing, Ask, DuckDuckGo, Yandex, Baidu, Exalead, Quora, Parsijoo, Dailymotion, Mojeek, Twitter and Youtube) and get the results as `json` or `xml`. The tool also stores the searched query string in a MongoDB database for analytical purposes.

[![Deploy to Docker Cloud](https://files.cloud.docker.com/images/deploy-to-dockercloud.svg)](https://cloud.docker.com/stack/deploy/?repo=https://github.com/fossasia/query-server) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/fossasia/query-server) [![Deploy on Scalingo](https://cdn.scalingo.com/deploy/button.svg)](https://my.scalingo.com/deploy?source=https://github.com/fossasia/query-server#master) [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/fossasia/query-server&branch=master)

## Table of Contents

- [API](#api)
- [Error Codes](#error-codes)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Contribute](#contribute)

## API

The API(s) provided by query-server are as follows:

` GET /api/v1/search/<search-engine>?query=query&format=format `

> *search-engine* : [`google`, `ask`, `bing`, `duckduckgo`, `yahoo`, `yandex`, `baidu`, `exalead`, `quora`, `youtube`, `parsijoo`, `mojeek`, `dailymotion`, `twitter`]

> *query* : query can be any string 

> *format* : [`json`, `xml`]

A sample query : `/api/v1/search/bing?query=fossasia&format=xml&num=10`

## Error Codes
    404 Not Found : Incorrect Search Engine, Zero Response
    400 Bad Request : query and/or format is not in the correct format
    500 Internal Server Error : Server Error from Search Engine

## Dependencies

* [MongoDB](https://www.mongodb.com)
* [Python 2.7](https://python.org)
    * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc)
    * [dicttoxml](https://github.com/quandyfactory/dicttoxml)
    * [Flask](http://flask.pocoo.org)
    * [pymongo](https://api.mongodb.com/python/current)
    * [requests](http://docs.python-requests.org)
* [Node.js](https://nodejs.org/en)
    * [bower.io](https://bower.io)

## Installation

1. [Local Installation](/docs/installation/local.md)

2. [Deployment on Heroku](/docs/installation/heroku.md)

3. [Deployment with Docker](/docs/installation/docker.md)

One-click Docker and Heroku deployment is also available:

[![Deploy to Docker Cloud](https://files.cloud.docker.com/images/deploy-to-dockercloud.svg)](https://cloud.docker.com/stack/deploy/?repo=https://github.com/fossasia/query-server) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/fossasia/query-server)

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/fossasia/query-server/issues)  For pull requests please read [Open Source Developer Guide and Best Practices at FOSSASIA](https://blog.fossasia.org/open-source-developer-guide-and-best-practices-at-fossasia/)

## License

This project is currently licensed under the Apache License version 2.0. A copy of `LICENSE` should be present along with the source code. To obtain the software under a different license, please contact [FOSSASIA](http://blog.fossasia.org/contact/).

