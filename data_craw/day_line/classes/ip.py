from bs4 import BeautifulSoup
import json
import random
import requests
import time

try:
    import download
except:
    from classes import download


# 构造 ip 池
class IPManage(object):

    def __init__(self, max_ip_num):
        self.ip_pool = []   # ip池
        f = open("const.json", "r", encoding='utf8')
        consts = json.loads(f.read())
        self.check_url = consts['check_url']        # 从常量文件提取 用于验证 ip 的 url
        self.pages = []                 # 已爬取过的 page 数组， 避免ip重复
        self.max_ip_num = max_ip_num    # 要爬取的 ip 总数   

    # 爬取 页面 page 全部的 ip
    def craw_ips_by_page(self, page):
        url = "https://www.xicidaili.com/nn/%s" % page
        downloader = download.Downloader()
        html_content = downloader.requests_get(url, "html")
        
        # 若返回 “0”， 可能是本机 ip 被封禁，尝试使用备用代理
        if html_content == "0":
            f = open("ips_copy.json", "r")
            ips = json.loads(f.read())
            for ip in ips:
                proxy_temp = {
                    "http": "http://%s:%s" % (ip['ip'], ip['port'])
                }
                print("本机ip不可用， 尝试 http://%s:%s" % (ip['ip'], ip['port']))
                try:
                    res = requests.get(url, timeout=1, proxies=proxy_temp)
                    if res.status_code == 200:
                        html_content = res.content.decode("utf-8","ignore")
                        break
                except:
                    continue

        soup = BeautifulSoup(html_content, 'html.parser')
        all_trs = soup.find("table", id="ip_list").find_all('tr')
        for tr in all_trs[1:]:
            tds = tr.find_all("td")
            ip = {
                'ip': tds[1].get_text(),
                'port': tds[2].get_text(),
                'type': tds[5].get_text()
            }
            # ip = tds[1].get_text()
            # 检查 ip 是否可用
            if self.check_ip(ip):
                self.ip_pool.append(ip)
            if len(self.ip_pool) >= self.max_ip_num:
                break
    
    # 获取 ip 池
    def craw_ips(self):
        max_page = 3000
        # 随机获取一个页码
        page = 5
        while True:
            page = random.randint(0, max_page)
            if page not in self.pages:
                break
        self.pages.append(page)
        print("当前爬取的ip页码为： ", page)
        self.craw_ips_by_page(page)
        with open("ip_pool.json","w") as f:
            json.dump(self.ip_pool,f)
        
        # 判断 ip 数量是否已足够
        if len(self.ip_pool) < self.max_ip_num:
            self.craw_ips()
        else:
            print("共抓取 %s 条ip" % len(self.ip_pool))

    # 检查代理ip是否可用
    def check_ip(self, ip):
        try:
            proxy_temp = {
                "http": "http://%s:%s" % (ip['ip'], ip['port'])
            }
            print(self.check_url, "---", "http://%s:%s  [%s]" % (ip['ip'], ip['port'], time.perf_counter()))
            res = requests.get(self.check_url, timeout=1, proxies=proxy_temp)
            if res.status_code == 200:
                return True
            else:
                return False
        except:
            return False
