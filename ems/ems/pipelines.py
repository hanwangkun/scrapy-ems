# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo;

class EmsPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGO_URI'),
                   crawler.settings.get('MONGO_DB'),
                   crawler.settings.get('MONGO_COLLECTION'));

    def __init__(self,mongo_uri,mongo_db,mongo_collection):
        self.mongo_uri = mongo_uri;
        self.mongo_db = mongo_db;
        self.mongo_collection = mongo_collection;

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri);
        self.db = self.client[self.mongo_db];

    def process_item(self, item, spider):
        return self.db[self.mongo_collection].insert(dict(item));

    def close_spider(self,spider):
         self.client.close();
