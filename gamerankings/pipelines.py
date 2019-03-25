# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
 
import pymongo

from gamerankings.items import ReviewItem

# this mongo db pipeline seems very general which means I can use it in lots of different projects
class GamerankingsPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
 
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!". format(data))
 
        if valid:
            if not isinstance(item, ReviewItem): # exclude except RecipeItem (for clean db)
                return item
            self.collection.insert(dict(item))
            log.msg("Quotes added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
 
        return item
