# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Paiza4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PaizaArticleItem(scrapy.Item):
    """
                企業名
                ポジション
                年収
                画像
                特徴
                url
                dbキー用のmd5url
    """
    name = scrapy.Field()
    position = scrapy.Field()
    income = scrapy.Field()
    images = scrapy.Field()
    images_path = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()