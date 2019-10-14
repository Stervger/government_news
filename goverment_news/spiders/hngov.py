# -*- coding: utf-8 -*-
from time import sleep
import scrapy
from goverment_news.items import GovermentNewsItem

class HngovSpider(scrapy.Spider):
    name = 'hngov'
    headers1 = {
        'Host': 'www.hainan.gov.cn',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def start_requests(self):
        a_list = ['5309/','ldhd/sj_']
        for a in a_list:
            for b in range(2,52):
                urls = list('http://www.hainan.gov.cn/hainan/' + a +'list3_'+ str(b) +'.shtml'.format(x) for x in range(5349))
                print(urls)
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/head/title//text()').extract()
        content = response.xpath('//*[@id="font"]/ucapcontent/p//text()').extract()
        publish_date = response.css('publishtime::text').extract()
        source = response.css('#ly::text').extract()

        if  len(content) != 0:
            items = GovermentNewsItem()
            items['title'] = title[0].replace('\r','').replace(' ','').replace('\n','').replace('_省府要闻_海南省人民政府网','')
            items['content'] = content
            items['publish_date'] = publish_date[0].replace('\r','').replace(' ','').replace('\n','')
            items['source'] = source
            yield items

        urls = response.css('a::attr(href)').extract()
        if len(urls) == 0:
            sleep(1)
        urls = list(filter(lambda x: x != '', urls))
        urls_company = list(filter(lambda x: '2019' in x, urls))

        for u in urls_company:

            if 'http' in u:
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})
            else:
                u = 'http://www.hainan.gov.cn' + u
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})

