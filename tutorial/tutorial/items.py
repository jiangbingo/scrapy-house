# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImgItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    img_url = scrapy.Field()
    img_name = scrapy.Field()

class DmozItem(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    city = scrapy.Field()
    type_name = scrapy.Field()
    url = scrapy.Field()
    wylb = scrapy.Field()
    xmts = scrapy.Field()
    jzlb = scrapy.Field()
    zxzk = scrapy.Field()
    hxwz = scrapy.Field()
    zxal = scrapy.Field()
    rjl = scrapy.Field()
    lhl = scrapy.Field()
    kpsj = scrapy.Field()
    jfsj = scrapy.Field()
    wyf = scrapy.Field()
    wygs = scrapy.Field()
    kfs = scrapy.Field()
    ysxkz = scrapy.Field()
    sldz = scrapy.Field()
    wydz = scrapy.Field()
    jtzk = scrapy.Field()
    fj = scrapy.Field()
    zdmj = scrapy.Field()
    jzmj = scrapy.Field()
    kgsj = scrapy.Field()
    jgsj = scrapy.Field()
    cqnx = scrapy.Field()

class TestItem(scrapy.Item):
    url = scrapy.Field()
