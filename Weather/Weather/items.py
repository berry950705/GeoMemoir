# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    location = scrapy.Field()
    weather_icon = scrapy.Field()
    weather_info = scrapy.Field()
    temperature = scrapy.Field()
    visibility = scrapy.Field()
    humidity = scrapy.Field()
    dew_point = scrapy.Field()
    date = scrapy.Field()
    cur_time = scrapy.Field()
