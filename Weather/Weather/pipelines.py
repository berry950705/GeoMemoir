# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from .settings import *


class WeatherPipeline:
    def process_item(self, item, spider):
        weather = {}
        weather['city'] = item['city']
        weather['location'] = item['location']
        weather['weather_icon'] = item['weather_icon']
        weather['weather_info'] = item['weather_info']
        weather['temperature'] = item['temperature']
        weather['visibility'] = item['visibility']
        weather['humidity'] = item['humidity']
        weather['dew_point'] = item['dew_point']
        weather['date'] = item['date']
        weather['cur_time'] = item['cur_time']
        print(weather)

        return item


class WeatherMysqlPipeline:
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset=MYSQL_CHARSET
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        update = 'update weather_weather set location=%s, weather_icon=%s, weather_info=%s, temperature=%s, visibility=%s, humidity=%s, dew_point=%s, date=%s, cur_time=%s where city=%s;'
        # ins = 'insert into weather_weather (city, location, weather_icon, weather_info, temperature, visibility, humidity, dew_point, date, cur_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        li = [
            item['location'],
            item['weather_icon'],
            item['weather_info'],
            item['temperature'],
            item['visibility'],
            item['humidity'],
            item['dew_point'],
            item['date'],
            item['cur_time'],
            item['city'],
        ]
        self.cursor.execute(update, li)
        self.db.commit()

        return item

    def close_spider(self, spider):
        self.db.close()
        self.cursor.close()

