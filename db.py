# -*- coding: utf-8 -*-
import os

import pymongo

db_url = 'mongodb+srv://{user}:{pwd}@{murl}/test?retryWrites=true&w=majority'
db_user = os.environ['muser']
db_pass = os.environ['mpass']
db_domain = os.environ['murl']
db_name = 'andev'
db_feeds_collection = 'feeds'
db_url = db_url.format(user=db_user, pwd=db_pass, murl=db_domain)
client = pymongo.MongoClient(db_url)

database = client[db_name]
feeds = database[db_feeds_collection]
