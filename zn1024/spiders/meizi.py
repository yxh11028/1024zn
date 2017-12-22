# -*- coding: utf-8 -*-
import scrapy
from zn1024.items import Zn1024Item
import os


class MeiziSpider(scrapy.Spider):
    name = 'meizi'
    allowed_domains = ['1024zn.com']
    _url = 'https://www.1024zn.com/meizitu/page/'
    # 从第一页开始爬取
    offset = 1
    start_urls = [_url + str(offset)]

    def parse(self, response):
        url_list = response.xpath('//h2[@class="grid-title"]/a/@href').extract()
        for url in url_list:
            url_offset = url.split('/')[-1].split('.')[0]
            # 自动生成目录
            os.mkdir('img/' + url_offset)
            yield scrapy.Request(url=url, meta={'path': url_offset}, callback=self.parse_item)

        if self.offset < 7:  # 总页数为 7
            self.offset += 1
        yield scrapy.Request(self._url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item_url_list = response.xpath('//img[@class="aligncenter"]/@src').extract()
        for url in item_url_list:
            item = Zn1024Item()
            item['url'] = url
            item['path'] = response.meta['path']

            yield item
