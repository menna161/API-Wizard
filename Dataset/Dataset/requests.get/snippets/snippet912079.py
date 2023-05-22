import requests
import json


def igxe_match(product_api, page, price, wear):
    ig_api = (('https://www.igxe.cn/product/trade/730/' + product_api) + '?page_no={}'.format(str(page)))
    api_request = requests.get(ig_api)
    if (api_request.status_code is 200):
        data = api_request.json()
        try:
            page_count = data['page']['page_count']
        except:
            return 2
        item_list = data['d_list']
        for item_detail in item_list:
            global item_name
            item_name = item_detail['name']
            if (float(item_detail['unit_price']) > price):
                return 2
            try:
                item_float = float(item_detail['exterior_wear'])
            except:
                item_float = 1
            if (item_float <= wear):
                print('{}   price:{}  wear:{}'.format(item_name, item_detail['unit_price'], item_float))
    else:
        print('igxe api failed')
        return 0
    return 1
