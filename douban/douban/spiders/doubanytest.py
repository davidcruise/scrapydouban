# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanytestSpider(scrapy.Spider):
    name = 'doubanytest'
    #allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for i in movie_list:
        	douban_item = DoubanItem()
        	douban_item['number'] = i.xpath('./div/div[1]/em/text()').extract_first()
        	douban_item['name'] = i.xpath('./div/div[2]/div[1]/a/span[1]/text()').extract_first()
        	content = i.xpath('./div/div[2]/div[2]/p[1]/text()').extract()[1].strip()
        	douban_item['introduce'] = "".join(content.split())
        	douban_item['star'] = i.xpath('./div/div[2]/div[2]/div/span[2]/text()').extract_first()
        	douban_item['evaluate'] = i.xpath('./div/div[2]/div[2]/div/span[4]/text()').extract_first()
        	douban_item['describe'] = i.xpath('./div/div[2]/div[2]/p[2]/span/text()').extract_first()
        	yield douban_item

        next_link = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        if next_link:
        	print(next_link)
        	next_link = next_link[0]
        	yield scrapy.Request('https://movie.douban.com/top250'+next_link,callback = self.parse)