from typing import Dict, Iterator
import requests
from lxml import etree


def get_search(*, keyword: str, pn: int, domain: str=None) -> Iterator[Dict]:
    keyword = ('site: {} {}'.format(domain, keyword) if domain else keyword)
    params = (('wd', keyword), ('pn', ((pn - 1) * 10)), ('oq', keyword), ('tn', 'baiduhome_pg'), ('ie', 'utf-8'), ('rsv_idx', '2'), ('rsv_pq', 'd09ea91a000533ad'), ('rsv_t', 'a741enhrt8jcViHd/8Q+gb0DnCzjIbctyKmpOkRk6BibYwnyQXvHFSqrZtTKeUHQlE4s'))
    response = requests.get('https://www.baidu.com/s', headers=headers, params=params, timeout=15)
    html = etree.HTML(response.text)
    items = html.xpath('//*/h3/a')
    for item in items:
        title = ''.join(item.xpath('.//text()'))
        href = item.xpath('./@href')[0]
        url = get_url(href)
        if (not url):
            continue
        if (domain and (domain not in url)):
            continue
        (yield {'title': title, 'url': url})
