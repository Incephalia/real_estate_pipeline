# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader 
from itemloaders.processors import TakeFirst, MapCompose 
from w3lib.html import remove_tags


class PropertyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    price_additional_description = scrapy.Field()
    property_type = scrapy.Field()
    suburb = scrapy.Field()
    bank_or_private = scrapy.Field()
    seller_or_status = scrapy.Field()
    property_images = scrapy.Field()
    
class Property24Item(scrapy.Item): 
    name = scrapy.Field() 
    price = scrapy.Field() 
    #description = scrapy.Field() 
    size = scrapy.Field()
    location = scrapy.Field() 
    image = scrapy.Field()