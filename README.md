# Query-Server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)

> Query server that stores a query or string on a server. This mini-tool can be used to process a query string. This string calls the search engine result scraper at [searss](https://github.com/fossasia/searss) and the output from the scraper is written to a file, named with the query string as file name.

<img src="workflow.gif" height=500px; />

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


## Usage

To run the query server: 
```
$ npm start
```
The search is prompted then.
```
Search for >>
```
Type query like (search engine choice)~(query).
For example: g~harambe or d~fossasia

### Options
```
  d~(query)         Use DuckDuckGo as search engine
  
  g~(query)         Use Google as search engine
                        
  b~(query)         Use Bing as search engine
                        
```

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/fossasia/query-server/issues)
