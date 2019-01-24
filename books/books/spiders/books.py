# -*- coding: utf-8 -*-

'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Date: 2019-01-24 16:35:29
@LastEditTime: 2019-01-24 17:31:40
@Description: 豆瓣读书全站爬虫
'''


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from books.items import BooksItem


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?icn=index-nav']
    rules = {
        Rule(LinkExtractor(allow='/tag/', restrict_xpaths="\\div[@class='artcle']"), follow=True),
        Rule(LinkExtractor(allow='/?start=\d+\&type=/', restrict_xpaths="\\div[@class='paginator']"), follow=True),
        
    }