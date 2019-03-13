#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: 西刺代理爬虫
@Date: 2019-03-06 09:54:13
'''

import logging

from lxml import etree
from config.config import get_log_config
from proxyPool.model.proxy import Proxy
from proxyPool.spiders.baseSpider import BaseSpider


class XiciSpider(BaseSpider):

    url = 'http://www.xicidaili.com/wt/1'
    # url = 'http://www.xicidaili.com/wn'

    agent = 'xici'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Referer': 'http://www.xicidaili.com/wt/1',
        'Referer': 'http://www.xicidaili.com/wn',
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Host': 'www.xicidaili.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
 
    }

    @classmethod
    def get_proxies(self):

        get_log_config()

        proxy_model_list = []

        print('正在爬取西刺代理......')

        response = super(XiciSpider, self).get_proxies()
        selector = etree.HTML(response.text)

        infos = selector.xpath('//tr[@class="odd"]')

        for i, info in enumerate(infos):
            try:
                ip = info.xpath('./td[2]/text()')[0]
                port = info.xpath('./td[3]/text()')[0]
                anonymity = info.xpath('./td[5]/text()')[0]
                http_type = info.xpath('./td[6]/text()')[0]
                area = info.xpath('./td[4]/a/text()')[0]
                speed = info.xpath('./td[7]/div/@title')[0]
                survival_time = info.xpath('./td[9]/text()')[0]

                print(ip + " | " + port + " | " + anonymity + " | " + http_type + " | " + area + " | " + speed + " | " + survival_time)

                proxy = Proxy()
                proxy.set_ip(ip)
                proxy.set_port(port)
                proxy.set_http_type(http_type)
                proxy.set_anonymity(anonymity)
                if area is None:
                    proxy.set_area("")
                else:
                    proxy.set_area(area)

                proxy.set_speed(speed)
                proxy.set_agent(self.agent)
                proxy.set_survival_time(survival_time)
                proxy_model_list.append(proxy)
                print(len(proxy_model_list))
            except Exception as e:
                logging.debug(e)
        
        logging.debug(f"抓取 {self.agent} 网站共计 {len(proxy_model_list)} 个代理")

        return proxy_model_list