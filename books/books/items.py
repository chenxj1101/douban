# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    publishing_house = scrapy.Field()
    publsh_time = scrapy.Field()
    page = scrapy.Field()
    price = scrapy.Field()
    ISBN = scrapy.Field()
    score = scrapy.Field()
    evaluation_num = scrapy.Field()
