#!/usr/bin/env python3

"""
query_cache.py -- Implements a caching system for query server based on MongoDB

Before sending a query to a remote search engine, use lookup() see if results
from that same search engine and query are already in the cache.  If so, then
print a cache hit message return the cached results.  If not, then use store()
to write the search engine, query, query results, and a datetime created into
the cache.  MongoDB will use the datetime to automatically delete out dated
query results.

Ideas for improvement:
* Add a lookup_count to see how often cache actually saves us time.
"""

import datetime as dt
import os

from pymongo import DESCENDING, MongoClient
from pymongo.errors import OperationFailure

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['query-server-v2']
db = db['queries']  # Automatically delete records that are older than one day
try:
    (db.create_index[('createdAt', DESCENDING)], expireAfterSeconds=60 * 60 * 24)
except OperationFailure:
    pass  # Database index already exists


def lookup(url):
    """return search result if the URL is in the db or None on a cache miss."""
    data = db.find_one({'url': url}) or {}
    return data.get('links', None)


def store(url, links):
    """write the URL, the links, and a UTC timestamp into the database."""
    db.delete_many({'url': url})  # remove all records for this URL
    db.insert({'url': url, 'links': links, 'createdAt': dt.datetime.utcnow()})


if __name__ == '__main__':
    url = 'test_url'
    print(lookup(url))
    store(url, 'a b c d e'.split())
    print(lookup(url))
