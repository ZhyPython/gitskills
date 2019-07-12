# -*- coding: utf-8 -*-
import scrapy
from scrapyspider.items import ProxyItem


class KdlspiderSpider(scrapy.Spider):
    name = 'kdlspider'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/75.0.3770.100 Safari/537.36',
               }
    start_urls = []

    def start_requests(self):
        for i in range(1, 6):
            self.start_urls.append('http://www.kuaidaili.com/free/inha/' + str(i) + '/')
            yield scrapy.Request(self.start_urls[i-1], headers=self.headers, dont_filter=True)

    def parse(self, response):
        item = ProxyItem()

        proxy_addrs = response.xpath('//table[@class="table table-bordered table-striped"]'
                                     '/tbody/tr')
        print('###############################')
        for proxy_addr in proxy_addrs:
            item['addr'] = proxy_addr.xpath('./td[@data-title="IP"]/text()'
                                            ).extract()[0]
            item['port'] = proxy_addr.xpath('./td[@data-title="PORT"]/text()'
                                            ).extract()[0]
            yield item
