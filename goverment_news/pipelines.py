# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class GovermentNewsPipeline(object):
    def __init__(self):
        pass
        # self.file = codecs.open(news.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        self.file = codecs.open('news.json', 'a', encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.close()
        return item