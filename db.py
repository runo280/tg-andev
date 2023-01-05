# -*- coding: utf-8 -*-
import os

import pymongo

db_url = 'mongodb+srv://{user}:{pwd}@{murl}/test?retryWrites=true&w=majority'
db_user = os.environ['muser']
db_pass = os.environ['mpass']
db_domain = os.environ['murl']
db_name = 'android'
db_feeds_collection = 'andev'
db_url_collection = 'andev_url'
db_url = db_url.format(user=db_user, pwd=db_pass, murl=db_domain)
client = pymongo.MongoClient(db_url)

database = client[db_name]
feeds = database[db_feeds_collection]
urls = database[db_url_collection]


def mark_as_read_all():
    unpublished_query = {'is_pub': False}
    set_published_query = {'$set': {'is_pub': True}}
    for x in feeds.find(unpublished_query):
        link = x['link']
        feeds.update_one({'link': link}, set_published_query)
