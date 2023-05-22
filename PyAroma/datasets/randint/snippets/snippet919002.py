import time
import random
import requests
from lxml import etree


def get_page(url):
    time.sleep(random.randint(1, 4))
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    et = etree.HTML(res.text)
    text_list = et.xpath('//*[@id="article"]/div/p/span/text()')
    result = []
    for text in text_list:
        if is_chinese(text[0]):
            pass
        elif (text[1] == '：'):
            result.append(text.split('：')[1])
        else:
            result.append(text.split(':')[1])
    save_text(result)
