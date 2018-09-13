# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EmsDistributeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    province = scrapy.Field();
    provinceName = scrapy.Field();
    city = scrapy.Field();
    cityName = scrapy.Field();
    dict = scrapy.Field();
    dictName = scrapy.Field();
    name = scrapy.Field();
    addr = scrapy.Field();
    tel = scrapy.Field();
    timestr = scrapy.Field();
