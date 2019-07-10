# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class ScrapyspiderPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['电影名称', '分数', '评论人数'])

    def process_item(self, item, spider):
        line = [item['movie_name'], item['score'], item['score_num']]
        self.ws.append(line)
        self.wb.save('E:\\scrapyspider\\scrapyspider\\job.xlsx')
        return item
