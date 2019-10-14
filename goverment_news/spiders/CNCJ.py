import  scrapy
from bs4 import BeautifulSoup
from goverment_news.items import GovermentNewsItem
class CNCJSpider(scrapy.Spider):
    name = 'CN'
    def start_requests(self):
        a_list = ['30611','30618','30619','30613','30902','30903','30621','31421']
        for a in a_list:
            urls = list('http://sousuo.gov.cn/column/'+a+'/{0}.htm'.format(x) for x in range(5349))
            print(urls)
            for url in urls:
                yield scrapy.Request(url=url,callback = self.parse)

    def parse(self, response):
        urls = response.xpath('/html/body/div[2]/div/div[2]/div[2]/ul/li/h4/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=url,callback=self.CN)
    def CN(self,response):
        item = GovermentNewsItem()
        item['content'] = response.xpath('//*[@id="UCAP-CONTENT"]/p//text()').extract()
        item['title']= response.xpath('//h1/text()').extract()
        item['publish_date']= response.xpath('//div[@class="pages-date"]/text()').extract()[:1]
        item['source']= response.xpath('//div[@class="pages-date"]/span/text()').extract()
        yield item


