# -*- coding: utf-8 -*-

'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Date: 2019-01-16 14:24:59
@LastEditTime: 2019-01-17 13:21:58
@Description: 豆瓣读书top250
'''

import re
from scrapy import Spider, Request
from douban.items import DoubanItem


class bookspidr(Spider):
    name = 'book250'
    allowed_domains = ["book.douban.com"]
    index = 0
    start_urls = [f'https://book.douban.com/top250?start={index}']

    def parse(self, response):
        item = DoubanItem()
        
        for i in range(1, 26):
            info = response.xpath(f"//div[@class='article']/div[@class='indent']/table[{i}]")
            item['book'] = info.xpath(".//div[@class='pl2']/a/@title")[0].extract()
            item['author'] = info.xpath(".//p[@class='pl']/text()")[0].extract().split(' / ')[0]
            item['time'] = info.xpath(".//p[@class='pl']/text()")[0].extract().split(' / ')[-2]
            price = info.xpath(".//p[@class='pl']/text()")[0].extract().split(' / ')[-1]
            if len(price) == 1:
                price = str(float(price))
            # print(price)
            item['price'] = float(re.findall(r"\d+.*?\d+", price)[0])
            item['star'] = float(info.xpath(".//div[@class='star clearfix']/span[@class='rating_nums']/text()").extract()[0])
            tmp = info.xpath(".//div[@class='star clearfix']/span[@class='pl']/text()")[0].extract()
            item['mark_num'] = int(re.findall(r"\d+", tmp)[0])
            # print(item['book'])

            yield item

        if self.index < 225:
            self.index += 25
            self.url = f'https://book.douban.com/top250?start={self.index}'

            yield Request(self.url, callback = self.parse)
