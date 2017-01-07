# query-server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)

> Query Server that stores a query string on a server.

This mini-tool can be used to process a query string. This string calls the Google search result scraper at [searss](https://github.com/fossasia/searss) and the output from the scraper is written to a file, named with the query string as file name.



# Requirements
* Python 2
* [Node.js](https://nodejs.org/en/)
* [PIP](https://pip.pypa.io/en/stable/installing/)
* [Mechanize](http://wwwsearch.sourceforge.net/mechanize/)
* [Feedgen](https://github.com/lkiesow/python-feedgen)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [html5lib](https://pypi.python.org/pypi/html5lib)

# Installing
Make sure you have [Nodejs](https://nodejs.org/en/) installed.
Running this tool requires installing the nodejs as well as python dependencies.
```
$ git clone https://github.com/fossasia/query-server.git 
$ cd query-server
$ npm install
$ pip install -r requirements.txt
```

# Running
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
