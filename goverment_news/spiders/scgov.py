# -*- coding: utf-8 -*-
from time import sleep
import scrapy
from goverment_news.items import GovermentNewsItem

class ScgovSpider(scrapy.Spider):
    name = 'scgov'
    headers1 = {
        'Host': 'www.sc.gov.cn',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    }

    def start_requests(self):
        a_list = ['10464/10797/jrsc_list_','12771/list_ft_']
        for a in a_list:
            for b in range(2,3):
                urls = list('http://www.sc.gov.cn/10462/' + a + str(b) +'.shtml'.format(x) for x in range(5349))
                print(urls)
                for url in urls:
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('/html/head/title//text()').extract()

        content = response.xpath('//*[@id="cmsArticleContent"]/ucapcontent/p//text()').extract()
        publish_date = response.xpath('//*[@id="articleattribute"]/li[1]//text()').extract()
        source = response.xpath('//*[@id="articleattribute"]/li[2]//text()').extract()

        if  len(content) != 0:
            items = GovermentNewsItem()
            items['title'] = title[0].replace('\r','').replace(' ','').replace('\n','')
            items['content'] = content
            items['publish_date'] = publish_date[0].replace('\r','').replace(' ','').replace('\n','')
            items['source'] = source
            yield items

        urls = response.css('#content a::attr(href)').extract()
        if len(urls) == 0:
            sleep(1)
        urls = list(filter(lambda x: x != '', urls))
        urls_company = list(filter(lambda x: '/2019' in x, urls))

        for u in urls_company:

            if 'http' in u:
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})
            else:
                u = 'http://www.sc.gov.cn' + u
                yield scrapy.Request(url=u, callback=self.parse, meta={'dont_merge_cookies': True})

