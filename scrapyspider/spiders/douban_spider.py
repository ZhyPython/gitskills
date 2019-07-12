from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieItem


class DoubanMovieRanking(Spider):
    name = 'douban_movie_ranking'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/75.0.3770.100 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        print('####################################')
        yield Request(url, headers=self.headers)

    def parse(self, response):
        """
        xpath 中的//指在这个HTML中所有的能够匹配的节点，
        .//指在当前目录下所有的能够匹配的节点，
        //a//b指在a节点下所有能够匹配到b（后代节点）
        //a/b指在a节点下能够匹配到的b子节点
        :param response
        :return: item
        """
        # 命令行中调试xpath语句
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        print('******************************************1')
        item = DoubanMovieItem()
        movies = response.xpath('//div[@id="content"]//ol[@class="grid_view"]/li')
        print(movies)
        # 从当前目录解析，注意.//中的.一定要加上
        for movie in movies:
            item['movie_name'] = movie.xpath(
                './/span[@class="title"]/text()'
            ).extract()[0].split()[0]
            item['score'] = movie.xpath(
                './/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="bd"]/div[@class="star"]/span[4]/text()'
            ).extract()[0]
            print('******************************************')
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)
