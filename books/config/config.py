#!/usr/bin/env python
# coding=UTF-8
'''
@Author: chenxj
@Github: https://github.com/chenxj1101
@Mail: ccj799@gmail.com
@Description: 配置文件
@Date: 2019-03-01 16:09:30
'''

import logging
import datetime


def get_log_config():
    LOG_LEVEL = logging.WARNING
    logging.getLogger("requests").setLevel(LOG_LEVEL)


    LOG_STORE_NAME = 'proxy_{}.txt'.format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

    fh = logging.FileHandler(encoding='utf-8', mode='w', filename='./' + LOG_STORE_NAME)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[fh],
        format='%(asctime)s %(filename)s[line:%(lineno)d]/%(levelname)s/  %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        
    )


MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'proxy'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'chenxj799'

THREADPOOL_NUM = 10

Validated_url = 'https://book.douban.com'

IF_USE_PROXY = False