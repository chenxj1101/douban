#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: 启动脚本
@Date: 2019-03-07 15:36:44
'''


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config.config import get_log_config
from proxyPool.ProxyPoolWorker import get_proxy_pool_worker


class SpiderManager(object):

    def __init__(self):
        self.isRunning = False
        self.setting = get_project_settings()
        # print(self.setting['BOT_NAME'])
        self.process = None



    def start_proxy_pool(self):
        get_proxy_pool_worker().start_work()


    def start_spider(self):
        self.process = CrawlerProcess(self.setting)
        for spider in spider_list:
            self.process.crawl(spider)
        self.process.start()


    def stop(self):
        self.isRunning = False
        get_proxy_pool_worker().stop_work()


    def start(self):
        self.start_proxy_pool()
        self.start_spider()


if __name__ == "__main__":
    get_log_config()

    manager = SpiderManager()
    # print(manager.setting['BOT_NAME'])
    spider_list = [manager.setting['BOT_NAME'], ]
    manager.start()