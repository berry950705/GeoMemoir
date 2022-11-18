import scrapy
from Weather.items import WeatherItem


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['www.timeanddate.com']
    start_urls = ['https://www.timeanddate.com/weather/?low=4']

    def parse(self, response, **kwargs):
        detail_links = response.xpath('//div[@class="row"]/div/table//tr/td/a/@href')

        link_list = []
        for item in detail_links:
            link_data = item.get()
            link = 'https://www.timeanddate.com' + link_data
            link_list.append(link)
        for url in link_list:
            yield scrapy.Request(url=url, callback=self.detail_page)

    def detail_page(self, response):
        weather = WeatherItem()

        city = response.xpath('//div[@id="bct"]/text()[3]').get()
        weather['city'] = city.strip() if city else response.xpath('//div[@id="bct"]/text()[2]').get().strip()

        weather['location'] = response.xpath('//div[@class="bk-focus__info"]/table//tr[1]//td/text()').get()

        icon_path = response.xpath('//*[@id="cur-weather"]/@src').get()
        weather['weather_icon'] = 'https:' + str(icon_path)

        weather['weather_info'] = response.xpath('//*[@id="qlook"]/p[1]/text()').get()

        temp_str = response.xpath('//table[@id="wt-5hr"]//tr[3]/td[1]/text()').get()
        temp_list = str(temp_str).split('\xa0')
        weather['temperature'] = ('').join(temp_list)

        vis_str = response.xpath('//div[@class="bk-focus__info"]/table//tr[4]//td/text()').get()
        vis_list = str(vis_str).split('\xa0')
        weather['visibility'] = (' ').join(vis_list)

        weather['humidity'] = response.xpath('//div[@class="bk-focus__info"]/table//tr[6]//td/text()').get()

        dew_str = response.xpath('//div[@class="bk-focus__info"]/table//tr[7]//td/text()').get()
        dew_list = str(dew_str).split('\xa0')
        weather['dew_point'] = ('').join(dew_list)

        date_time = response.xpath('//div[@class="bk-focus__info"]/table//tr[2]//td/text()').get()
        weather['date'] = date_time.split('at')[0].strip()
        cur_time_str = date_time.split('at')[1].strip()
        weather['cur_time'] = cur_time_str.split(' ')[0].strip()

        if weather['city']:
            yield weather

