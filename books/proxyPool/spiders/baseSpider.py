#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: 爬虫基类
@Date: 2019-03-04 16:18:35
'''

from proxyPool.requester import requestEnginer

class BaseSpider(object):

    url = ""
    headers = {}

    def __init__(self):
        pass

    @classmethod
    def get_proxies(self):
        if self.headers is None:
            responese = requestEnginer.do_get(self.url)
        else:
            responese = requestEnginer.do_get(self.url, self.headers)
        return responese