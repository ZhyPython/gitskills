import re
import json

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieAjax


class DoubanAjaxSpider(Spider):
    name = 'douban_ajax'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/75.0.3770.100 Safari/537.36', }

    def start_requests(self):
        url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        datas = json.loads(response.body)
        item = DoubanMovieAjax()
        if datas:
            for data in datas:
                item['ranking'] = data['rank']
                item['movie_name'] = data['title']
                item['score'] = data['score']
                item['score_num'] = data['vote_count']
                yield item

        # 若datas存在数据则对下一页进行采集, group函数将匹配字符串中的()所匹配的内容放入一个组内，
        # group(0)是整个匹配字符串的匹配内容，group(1)是第一个中括号()匹配的内容
        # print(response.url)
        page_num = re.search(r'start=(\d+)', response.url).group(1)
        if int(page_num) < 80:
            page_num = 'start=' + str(int(page_num)+20)
            next_url = re.sub(r'start=\d+', page_num, response.url)
            yield Request(next_url, headers=self.headers)
