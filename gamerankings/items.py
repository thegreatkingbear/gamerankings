# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    crumbs = scrapy.Field()
    review_url = scrapy.Field()
    pass

class ReviewItem(scrapy.Item):
    game_name = scrapy.Field()
    game_tag = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    score = scrapy.Field()
    pass