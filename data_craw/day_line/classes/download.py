import requests
import urllib
import http.client
import csv
from bs4 import BeautifulSoup
import json
import random
import os
import time

try:
    import ip as ipmanage
except:
    from classes import ip as ipmanage

class Downloader(object):

    def __init__(self, ip_pool=[]):
        self.ip_pool = ip_pool
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
    
    # 初始化 IP 池
    def init_ip_pool(self, ip_num=80):
        try:
            t = os.path.getmtime("ip_pool.json")
            flag = True
        except:
            flag = False
        if flag and time.time() - t < 300:       # ip池未过期, 调用本地缓存
            f = open("ip_pool.json", "r", encoding='utf8')
            self.ip_pool = json.loads(f.read())
        else:
            ip_manage = ipmanage.IPManage(max_ip_num=ip_num)
            ip_manage.craw_ips()
            self.ip_pool = ip_manage.ip_pool

    # get 请求
    def requests_get(self, url, type, data=None):
        response = requests.get(url=url, headers=self.headers, data=data)
        if response.status_code == 200:
            # request successfully
            if type == "img":
                # 获取图片
                return response.content
            if type == "html":
                html = response.content
                # html_content = str(html,'utf-8')
                html_content = html.decode("utf-8","ignore")
                return html_content
            if type == "text":
                return response.text
        else:
            print("Request Falied For Code: %s" % response.status_code)
            return "0"

    # post 请求
    def requests_post(self, url, type, data=None):
        response = requests.post(url=url, headers=self.headers, data=data)
        if response.status_code == 200:
            # request successfully
            if type == "img":
                # 获取图片
                return response.content
            if type == "html":
                html = response.content
                # html_content = str(html,'utf-8')
                html_content = html.decode("utf-8","ignore")
                return html_content
            if type == "text":
                return response.text
        else:
            print("Request Falied For Code: %s" % response.status_code)

    # 下载网易财经 csv 文件至指定目录
    def download_netease_csv(self, url, filepath):
    
        try:
            ip = random.choice(self.ip_pool)
            # 设置代理
            proxy_temp = {
                "https": "https://%s:%s" % (ip['ip'], ip['port'])
            }
            r = requests.get(url, proxies=proxy_temp)
            with open(filepath, 'wb') as content:
                content.write(r.content)
        except:
            print("error to save %s" % filepath)

# if __name__ == "__main__":
#     d = Downloader()
#     d.init_ip_pool(10000)