# Query-Server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)
[![Dependency Status](https://david-dm.org/fossasia/query-server.svg)](https://david-dm.org/ossasia/query-server)
> Query server that stores a query or string on a server. This mini-tool can be used to process a query string. This string calls the search engine result scraper at [searss](https://github.com/fossasia/searss) and the output from the scraper is written to a file, named with the query string as file name.

## Table of Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [Options](#options)
- [Contribute](#contribute)

## Dependencies  

* Python 2.x or Python 3.x
* [Node.js](https://nodejs.org/en/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [Feedgen](https://github.com/lkiesow/python-feedgen)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)


## Installation

Make sure you have [Nodejs](https://nodejs.org/en/) installed.
Running this tool requires installing the nodejs as well as python dependencies.

```
$ git clone https://github.com/fossasia/query-server.git 
$ cd query-server
$ npm install
$ pip install -r requirements.txt
```

To set up MongoDB on your server : 
```
 $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
 $ echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
 $ sudo apt-get update
 $ sudo apt-get install -y mongodb-org
 $ sudo service mongod start
```

## Usage

To run the query server: 
```
$ npm start
```

Then head over to **<http://localhost:7001>** in your browser.

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/fossasia/query-server/issues)