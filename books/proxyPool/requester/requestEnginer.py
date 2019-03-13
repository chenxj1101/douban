#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: request_setting
@Date: 2019-03-04 14:54:21
'''


import logging
import requests
import threadpool
from requests.adapters import HTTPAdapter
from config.config import Validated_url
from config.config import THREADPOOL_NUM


session = requests.Session()
available_proxy_list = []


def do_get(url, headers, *proxies):
    timeout = 3

    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))


    if headers is None:
        if proxies is None:
            response = session.get(url, timeout=timeout)
            return response
        else:
            response = session.get(url, proxies=proxies, timeout=timeout)
            return response
    else:
        if proxies is None:
            response = session.get(url, headers=headers, timeout=timeout)
            return response
        else:
            response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
            return response


def filter_unavailable_proxy(proxy_list):
    available_proxy_list.clear()

    pool = threadpool.ThreadPool(THREADPOOL_NUM)
    pool_requests = threadpool.makeRequests(filter_proxy, proxy_list, save_filter_proxy)
    for req in pool_requests:
        pool.putRequest(req)
    pool.wait()

    logging.debug("=====  经过过滤后剩下 " + str(len(available_proxy_list)) + "个代理  =====")
    return available_proxy_list


def filter_proxy(model):

    url = Validated_url

    http_type = model.get_http_type()
    ip = model.get_ip()
    port = model.get_port()

    proxies = {
        'http_type': http_type.lower() + "://" + ip + ":" + str(port)
    }
    
    try:
        response = do_get(url, proxies)

        if response.status_code == 200:
            return model
        else:
            return None
    except Exception as e:
        logging.debug(e)


def save_filter_proxy(requests, filter_model):
    
    if filter_model is not None:
        available_proxy_list.append(filter_model)