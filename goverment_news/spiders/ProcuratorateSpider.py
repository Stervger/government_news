from time import sleep

import scrapy
import re
from goverment_news.items import GovermentNewsItem

class ProcuratorateSpider(scrapy.Spider):
    headers1 = {
        'Host': 'www.spp.gov.cn',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
    }
    name = "procuratorate_news"

    def start_requests(self):
        urls = [
            'https://www.spp.gov.cn/',
            # 'https://www.spp.gov.cn/spp/gjybs/index.shtml'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers1, meta={'dont_merge_cookies': True})

    def parse(self, response):
        # print(response)
        title = response.css('.detail_tit::text').extract()#标题
        #publish_date = response.css('.detail_extend1 fl::text').extract()#出版日期
        content = response.css('#fontzoom p::text').extract()#内容
        publish_date = response.xpath('//div[@class="detail_extend1 fl"]//text()').extract_first()

        if len(title) != 0:
            if len(publish_date) != 0:
                    if len(content) != 0:

                            news = GovermentNewsItem()
                            news['title'] = title[0]
                            #news['publish_date'] = publish_date[0][4:14]
                            news['content'] = content
                            news['publish_date'] = re.findall(r'时间：(\d+-\d+\-\d+).*?来源：.*?',publish_date,re.S)
                            news['source'] = re.findall(r'时间.*?来源：(\w+)',publish_date,re.S)
                            yield news

        page = response.css('a::attr(href)').extract()
        if len(page) == 0:
            sleep(1)
        page = list(filter(lambda x: x != '', page))
        page_company = list(filter(lambda x: '/spp/' in x, page))

        for p in page_company:

            if("http" in p):
                yield  scrapy.Request(url=p, callback=self.parse, headers=self.headers1, meta={'dont_merge_cookies': True})
            # a=requests.get(p,headers=self.headers1)
            # self.log(a)
            else:
                p="https://www.spp.gov.cn/"+p
            yield scrapy.Request(url=p, callback=self.parse, headers=self.headers1, meta={'dont_merge_cookies': True})

