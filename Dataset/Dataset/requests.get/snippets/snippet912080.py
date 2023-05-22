import requests
import json


def buff_match(name, product_api, price, wear):
    buff_api = 'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num=1&page_size=100'.format(product_api)
    api_request = requests.get(buff_api)
    if (api_request.status_code is 200):
        data = api_request.json()
        item_list = data['data']['items']
        for item_detail in item_list:
            try:
                item_wear = item_detail['asset_info']['paintwear']
            except:
                item_wear = 1
            item_price = item_detail['price']
            if (float(item_price) > price):
                return 0
            if (float(item_wear) <= wear):
                print('{}   price:{}  wear:{}'.format(name, item_price, item_wear))
    else:
        print('buff api failed')
        return 0
    return 1
