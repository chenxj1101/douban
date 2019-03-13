#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: IP代理池模块，主入口
@Date: 2019-03-06 13:12:32
'''

import random

from proxyPool.dbManger.proxyDBmanger import ProxyDBmanager
from proxyPool.spiders.data5uSpider import Data5uSpider
from proxyPool.spiders.kuaidailiSpider import KuaidailiSpider
from proxyPool.spiders.xiciSpider import XiciSpider
from proxyPool.requester import requestEnginer
from apscheduler.schedulers.background import BackgroundScheduler


class proxyPoolWorker(object):

    __MIN_PROXY_NUM = 15

    def __init__(self):

        self.__first = True
        self.dbmanager = ProxyDBmanager()
        self.dbmanager.drop_proxy_table()
        self.dbmanager.create_proxy_table()

    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            new = super(proxyPoolWorker,cls)
            cls.__instance = new.__new__(cls, *args)
        return cls.__instance


    def start_work(self):
        self.crawl_proxy_web()

        scheduler = BackgroundScheduler()
        scheduler.add_job(self.__check_ip_availability_task, 'interval', minutes=10)
        scheduler.start()

    
    def __check_ip_availability_task(self):
        pass

    
    def crawl_proxy_web(self):

        spiders = [
            XiciSpider,
            # Data5uSpider,
            KuaidailiSpider,
        ]

        spiders = random.choice(spiders)
        models = spiders.get_proxies()
        filtered_models = requestEnginer.filter_unavailable_proxy(models)
        for each in filtered_models:
            self.dbmanager.insert_proxy_table(each)

    
    def select_proxy_data(self):
        proxy = self.dbmanager.select_random_proxy()
        if proxy is not '':
            proxy = self.dbmanager.select_random_proxy()
            return proxy


    def plus_proxy_faild_time(self, ip):
        self.dbmanager.plus_proxy_faild_time(ip)

    
    def stop_work(self):
        self.dbmanager.close_connection()


proxy_pool = proxyPoolWorker()


def get_proxy_pool_worker():
    return proxy_pool
