#!/bin/env python
import requests
from bs4 import BeautifulSoup
import random
import os
import sys

sys.path.append(os.path.dirname(__file__))
import util

f = open('config/proxy_pool.txt', 'w')


class GetProxyIP:

    def __init__(self, page=10):
        self._page = page
        self.url_head = 'https://www.kuaidaili.com/free/inha/'
        self.max = 100
        self.cur = 0

    def get_proxy_pool(self):
        """
        get resouce proxy ip pool
        :return: proxy
        """
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        for pagenum in range(1, self._page):
            url = self.url_head + str(pagenum)
            print('url', url)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}
            response = util.get_requests(url, headers)
            soup = BeautifulSoup(response.text, "html.parser")
            soup_tr = soup.find_all('tr')
            for item in soup_tr:
                try:
                    soup_td = item.find_all('td')
                    # 获取到网页的代理IP信息
                    if "HTTPS" in str(soup_td[3]):
                        ip = 'https://{ip}:{port}'.format(ip=soup_td[0].text, port=soup_td[1].text)
                    else:
                        ip = 'http://{ip}:{port}'.format(ip=soup_td[0].text, port=soup_td[1].text)
                    proxy = self.is_right_proxy(ip)
                    if proxy is None:
                        continue
                    else:
                        print('add proxy: {}'.format(str(proxy)))
                        f.writelines("{}\n".format(str(proxy)))
                        self.cur += 1
                        if self.cur > self.max:
                            break
                except IndexError:
                    pass

    def is_right_proxy(self, ip):
        """
        check available ip
        :param res_pool:
        :return:right_pool list
        """
        print("check IP {}".format(ip))
        if 'https' in ip:
            proxies = {'https': ip}
        else:
            proxies = {"http": ip}
        check_urllist = ['http://www.baidu.com', 'http://www.taobao.com', 'https://cloud.tencent.com/']
        try:
            response = requests.get(random.choice(check_urllist), proxies=proxies, timeout=1)
            # 判断筛选可用IP
            print("response.status_code", response.status_code)
            if response.status_code:
                return proxies
        except Exception as e:
            return None


if __name__ == '__main__':
    # 实例化类，可以传入page
    proxyhelper = GetProxyIP(100)
    proxyhelper.get_proxy_pool()
    f.close()
