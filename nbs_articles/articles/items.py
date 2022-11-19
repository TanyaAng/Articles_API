# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlesItem(scrapy.Item):
    date = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    labels = scrapy.Field()
    links = scrapy.Field()
