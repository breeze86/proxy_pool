#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@File       :   wandouip.py
@Contact    :   breeze.yang.tech@linkkt.one
@Project    :   proxy_pool

@Modify Time        @Author     @Version    @Desc
-----------------   ---------   ---------   ---------------------
2020/4/16 14:44     Breeze      0.0.1       None     
"""
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import json

BASE_URL = 'http://api.wandoudl.com/api/ip'


# MAX_PAGE = 5


class WanDouIpCrawler(BaseCrawler):
    """
    WanDouIpCrawler crawler, http://api.wandoudl.com/api/ip
    """
    urls = [BASE_URL]
    kwargs = {'params': {
            'app_key': 'f0c0707bac3282d147ecd9458c833d70',
            'pack': 210641,
            'num': 2,
            'xy': 1,
            'type': 2,
            'lb': r'\r\n',
            'mr': 1,
        }}

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        response = doc('p').text()
        trs = json.loads(response)['data']
        for tr in trs:
            host = tr['ip']
            port = tr['port']
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    # 测试代码
    crawler = WanDouIpCrawler()
    for proxy in crawler.crawl():
        print(proxy)
