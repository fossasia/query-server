# Query-Server

[![Build Status](https://travis-ci.org/fossasia/query-server.svg?branch=master)](https://travis-ci.org/fossasia/query-server)
[![Dependency Status](https://david-dm.org/fossasia/query-server.svg)](https://david-dm.org/ossasia/query-server)
[![Join the chat at https://gitter.im/fossasia/query-server](https://badges.gitter.im/fossasia/query-server.svg)](https://gitter.im/fossasia/query-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![codecov](https://codecov.io/gh/fossasia/query-server/branch/master/graph/badge.svg)](https://codecov.io/gh/fossasia/query-server)

The query server can be used to search a keyword/phrase on a search engine (Google, Yahoo, Bing, Ask, DuckDuckGo, Baidu, Exalead, Quora, Parsijoo, Dailymotion, Mojeek and Youtube) and get the results as `json`, `xml` or `csv`. The tool also stores the searched query string in a MongoDB database for analytical purposes.

[![Deploy to Docker Cloud](https://files.cloud.docker.com/images/deploy-to-dockercloud.svg)](https://cloud.docker.com/stack/deploy/?repo=https://github.com/fossasia/query-server) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/fossasia/query-server) [![Deploy on Scalingo](https://cdn.scalingo.com/deploy/button.svg)](https://my.scalingo.com/deploy?source=https://github.com/fossasia/query-server#master) [![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/fossasia/query-server&branch=master)

## Table of Contents

- [Test Deployment](#test-deployment)
- [API](#api)
- [Error Codes](#error-codes)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Contribute](#contribute)

## Test Deployment

A test deployment of the project is available here: https://query-server.herokuapp.com

## API

The API(s) provided by query-server are as follows:

` GET /api/v1/search/<search-engine>?query=query&format=format `

> *search-engine* : [`google`, `ask`, `bing`, `duckduckgo`, `yahoo`, `baidu`, `exalead`, `quora`, `youtube`, `parsijoo`, `mojeek`, `dailymotion`]

> *query* : query can be any string 

> *format* : [`json`, `xml`, `csv`]

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


## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/fossasia/query-server/issues)  For pull requests please read [Open Source Developer Guide and Best Practices at FOSSASIA](https://blog.fossasia.org/open-source-developer-guide-and-best-practices-at-fossasia/)

## Keeping A Fork Up To Date

#### 	1. Configuring a remote for a fork
You must configure a remote that points to this repository in Git to sync changes made in this repository with the fork.
1. Open Terminal (Linux/Mac)
	Open Git Bash (Windows)
2. List the current configured remote repository for your fork.

		  $ git origin -v
		  origin  https://github.com/YOUR_USERNAME/query-server.git (fetch)
		  origin  https://github.com/YOUR_USERNAME/query-server.git (push)

3. Add this as a new remote upstream repository.

		  $ git remote add upstream https://github.com/fossasia/query-server.git

4. Verify new upstream repository.

	  	  $ git remote -v
		  origin    https://github.com/YOUR_USERNAME/query-server.git (fetch)
		  origin    https://github.com/YOUR_USERNAME/query-server.git (push)
		  upstream  https://github.com/fossasia/query-server.git (fetch)
		  upstream  https://github.com/fossasia/query-server.git (push)


#### 	2. Syncing a fork
1. Open Terminal (Linux/Mac)
	Open Git Bash (Windows)
2. Change the current working directory to your forked project.
3. Fetch the branches and their respective commits from the upstream repository.
 Commits to master will be stored in a local branch, upstream/master.
 
		  $ git fetch upstream
		  remote: Counting objects: 75, done.
		  remote: Compressing objects: 100% (53/53), done.
		  remote: Total 62 (delta 27), reused 44 (delta 9)
		  Unpacking objects: 100% (62/62), done.
		  From https://github.com/fossasia/query-server 
			* [new branch]      master     -> upstream/master

4. Check out your fork's local master branch.

		  $ git checkout master
		  Switched to branch 'master'

5. Merge the changes from upstream/master into your local master branch. This brings your fork's master branch into sync with the upstream repository, without losing your local changes.

		  $ git merge upstream/master
		  Updating a442332..5fdff1f
		  Fast-forward
		  README                    |    19 -------
		  README.md                 |    71 ++++++
		  5 files changed, 71 insertions(+), 19 deletions(-)
		  delete mode 100644 README
		  create mode 100644 README.md

If your local branch didn't have any unique commits, Git will instead perform a "fast-forward":

		  $ git merge upstream/master
		  Updating 34e91da..16c56ad
		  Fast-forward
		    README.md                 |    5 +++--
		    1 file changed, 3 insertions(+), 2 deletions(-)

## License

This project is currently licensed under the Apache License version 2.0. A copy of `LICENSE` should be present along with the source code. To obtain the software under a different license, please contact [FOSSASIA](http://blog.fossasia.org/contact/).

