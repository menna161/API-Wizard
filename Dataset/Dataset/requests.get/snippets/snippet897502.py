import vthread
import os, re, json, time, queue, traceback
import requests
from lxml import etree


@pool_gets
def crawl(page):
    url = 'https://www.baidu.com/s?wd=123&pn={}'.format((page * 10))
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, ', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Cookie': 'BAIDUID=AEFC0BF73865D50E79A88E1D572BDFFC:FG=1; ', 'Host': 'www.baidu.com', 'Pragma': 'no-cache', 'Referer': 'https://www.baidu.com/', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
    s = requests.get(url, headers=headers)
    if (s.history and (s.history[0].status_code == 302)):
        print('retrying {}. curr statcode:{}'.format(s.history[0].request.url, s.status_code))
        crawl(page)
        return
    tree = etree.HTML(s.content.decode('utf-8'))
    for x in tree.xpath('//div/h3[@class="t"]/parent::*'):
        d = {}
        d['href'] = x.xpath('./h3/a[1][@target]/@href')[0]
        d['title'] = x.xpath('string(./h3[@class="t"])').strip()
        datapipe.put(d)
