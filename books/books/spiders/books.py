# -*- coding: utf-8 -*-

'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Date: 2019-01-24 16:35:29
@LastEditTime: 2019-02-01 10:00:23
@Description: 豆瓣读书全站爬虫
'''


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from books.items import BooksItem


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag/?icn=index-nav']

    rules = {
        # Rule(LinkExtractor(allow=r'/tag/', restrict_xpaths="//div[@class='artcle']"), follow=True),
        Rule(LinkExtractor(allow=r'/tag/',restrict_xpaths="//div[@class='article']"),follow=True),
        # Rule(LinkExtractor(allow='\?start=\d+\&type=', restrict_xpaths="//div[@class='paginator']"), follow=True),
        Rule(LinkExtractor(allow=r'\?start=\d+\&type=',restrict_xpaths="//div[@class='paginator']"),follow=True),
        # Rule(LinkExtractor(allow='/subject/\d+/$', restrict_xpaths="//ul[@class='subject-list']"), callback='parse_item')
        Rule(LinkExtractor(allow=r'/subject/\d+/$',restrict_xpaths="//ul[@class='subject-list']"),callback='parse_item')
    }


    def parse_item(self, response):
        item = BooksItem()
        # print(response.status)
        if response.status == 200:
            # try:
                item['url'] = response.url
                item['name'] = response.xpath("//div[@id='wrapper']/h1/span/text()").extract_first()
                # item['author'] = response.xpath("//div[@id='info']/a[1]/text()")[0].extract().replace('\n' ,'').replace(' ', '')
                _info = response.xpath("//div[@id='info']//text()").extract()
                info = [s.strip() for s in _info if s.strip() != '']
                # item['publishing'] = info[0]
                # item['publsh_time'] = info[-5]
                # item['page'] = info[-4]
                # item['price'] = info[-3]
                # item['ISBN'] = info[-1]
                item['author'] = ''
                item['publishing'] = ''
                item['publish_time'] = ''
                item['page'] = ''
                item['price'] = ''
                item['ISBN'] = ''
                item['score'] = 0.0
                item['evaluation_num'] = 0
                if '作者' in info:
                    item['author'] = info[info.index('作者') + 2]
                if '作者:' in info:
                    item['author'] = info[info.index('作者:') + 1]
                if '出版社:' in info:
                    item['publishing'] = info[info.index('出版社:') + 1]
                if '出版年:' in info:
                    item['publish_time'] = info[info.index('出版年:') + 1]
                if '页数:' in info:
                    item['page'] = info[info.index('页数:') + 1]
                if '定价:' in info:
                    item['price'] = info[info.index('定价:') + 1]
                if 'ISBN:' in info:
                    item['ISBN'] = info[info.index('ISBN:') + 1]
                if not response.xpath("//div[@class='rating_sum']/span/a/text()").extract():
                    item['score'] = response.xpath("//div[@class='rating_self clearfix']/strong/text()")[0].extract().strip()
                    item['evaluation_num'] = response.xpath("//a[@class='rating_people']/span/text()")[0].extract()
                yield item
            # except:
            #     print(f'{response.url} have some problem')
        else:
            print('***********************something  wrong***********************')

