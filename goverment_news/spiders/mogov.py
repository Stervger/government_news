# -*- coding: utf-8 -*-
from time import sleep
from urllib.parse import urlencode
import scrapy
from goverment_news.items import GovermentNewsItem
import re


class JiangxiSpider(scrapy.Spider):
    name = 'mogov'
    def start_requests(self):
        url='http://www.jiangxi.gov.cn/col/col393/index.html?'
        for a in range(2,80):
            p={'uid': '45663',
               'pgeNum':a}
            yield scrapy.Request(url=(url+urlencode(p)), callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/head/title//text').extract()
        content = response.css('#zoom p::text').extract()
        source = response.xpath('//*[@id="zoom"]/div/font[1]/text()[2]').extract()
        time = re.findall(r'<font>发布时间：(.*?)</font>', response.text, re.M)

        if  len(content) != 0:
            items = GovermentNewsItem()
            items['title'] = title[0].replace('<p>','').replace('\r','').replace(' ','').replace('</p>','').replace('\n','')
            items['content'] = content
            items['time'] = time
            items['source'] = source
            yield items

        urls = re.findall(r'<a href="(.*?)" tar',response.text,re.M)
        print(urls)
        urls = list(filter(lambda x: x != '', urls))
        urls_company = list(filter(lambda x: '/art/' in x, urls))

        for u in urls_company:
            yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})
