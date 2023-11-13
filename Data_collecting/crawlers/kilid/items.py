# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    price_per_meter = scrapy.Field()
    address = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    properties = scrapy.Field()
    func = scrapy.Field()
    type = scrapy.Field()
    meterage = scrapy.Field()
    floor = scrapy.Field()
    date = scrapy.Field()
    bedroom = scrapy.Field()
    parking = scrapy.Field()
    age = scrapy.Field()
    facilities = scrapy.Field()