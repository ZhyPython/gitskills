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
        url = 'https://movie.douban.com/chart'
        print('####################################')
        yield Request(url, headers=self.headers)

    def parse(self, response):
        '''
        xpath 中的//指在这个HTML中所有的能够匹配的节点，
        .//指在当前目录下所有的能够匹配的节点，
        //a//b指在a节点下所有能够匹配到b（后代节点）
        //a/b指在a节点下能够匹配到的b子节点
        :param response:
        :return: item
        '''
        print('******************************************1')
        item = DoubanMovieItem()
        movies = response.xpath('//div[@id="content"]//div[@class="indent"]//table')
        print(movies)
        for movie in movies:
            item['movie_name'] = movie.xpath(
                './/a[@class=""]/text()'
            ).extract()[0].split()[0]
            item['score'] = movie.xpath(
                './/div[@class="star clearfix"]/span[@class="rating_nums"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star clearfix"]/span[@class="pl"]/text()'
            ).extract()[0]
            print('******************************************')
            yield item
