#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: 请求处理工具
@Date: 2019-03-06 10:56:37
'''

import logging
from proxyPool.ProxyPoolWorker import get_proxy_pool_worker


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy_address = get_proxy_pool_worker().select_proxy_data()
        logging.debug(f"===== ProxyMiddleware get a random_proxy: 【 {proxy_address} 】")
        request.meta['proxy'] = proxy_address


    def process_exception(self, request, exception, spider):
        pass


class CatchExceptionMiddleware(object):
    def process_exception(self, request, Exception, spider):
        try:
            proxy = request.meta['proxy']
            if 'http://' in proxy:
                proxy = proxy.replace('http://', '')
            else:
                proxy = proxy.replace('https://', '')

            get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
        except Exception as e:
            logging.debug("===  访问页面: " + request.url + " 出现异常. \n %s", e)

    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            try:
                proxy = request.meta['proxy']
                if 'https://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')

                get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
            except KeyError:
                logging.debug(f"===  无法正常访问到的页面: {response.url}  ===")
        return response



class RetryMiddleware(object):
    def process_exception(self, request, exception, spider):
        try:
            proxy = request.meta['proxy']
            if 'http://' in proxy:
                proxy = proxy.replace('http://', '')
            else:
                proxy = proxy.replace('https://', '')
            
            get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])

        except Exception as e:
            logging.debug(f"===  访问页面: {request.url} 出现异常。 \n{e}")


    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            try:
                proxy = request.meta['proxy']
                if 'http://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')

                get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
            except KeyError:
                logging.debug("===  无法正常访问到的页面: {response.url}  ===")
        return response