# -*- coding: utf-8 -*-
from time import sleep

import scrapy

from goverment_news.items import GovermentNewsItem


class CqgovSpider(scrapy.Spider):
    name = 'cqgov'
    headers1 = {
        'Host': 'www.cq.gov.cn',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def start_requests(self):
        for a in range(80):
            urls = list('http://www.cq.gov.cn/zwxx/jrcq_' + str(a).format(x) for x in range(5349))
            print(urls)
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/body/div/div[3]/div/div/article/div/h2//text()').extract()

        content = response.xpath('/html/body/div/div[3]/div/div/article/div/div[2]//text()').extract()

        if len(title) and len(content) != 0:
            items = GovermentNewsItem()
            items['title'] = title[0].replace('\r','').replace(' ','').replace('\n','')
            items['content'] = content[1].replace('\r','').replace(' ','').replace('\n','')
            items['publish_date'] = response.xpath('/html/body/div/div[3]/div/div/article/div/div[1]/span/span[2]//text()').extract()
            items['source'] = response.xpath('/html/body/div/div[3]/div/div/article/div/div[1]/span/span[1]//text()').extract()
            yield items

        urls = response.css('a::attr(href)').extract()
        if len(urls) == 0:
            sleep(1)
        urls = list(filter(lambda x: x != '', urls))
        urls_company = list(filter(lambda x: 'content_' in x, urls))

        for u in urls_company:

            if 'http' in u:
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})
            else:
                u = 'http://www.cq.gov.cn'+u
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})

