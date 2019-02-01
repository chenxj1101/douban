# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from books.settings import MongoDB_COLLECTION,MongoDB_DB,MongoDB_HOST,MongoDB_PORT,MongoDB_USER,MongoDB_PSW

host = MongoDB_HOST
port = MongoDB_PORT
db = MongoDB_DB
coll = MongoDB_COLLECTION
user = MongoDB_USER
pwd = MongoDB_PSW

class BooksPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db]
        self.db.authenticate(user, pwd)
        self.collection = self.db[coll]

    def process_item(self, item, spider):
        postItem = dict(item)
        self.collection.insert_one(postItem)
        return item
