import uuid
import requests
from btp.util import req


def push(aria2_jsonrpc_url, aria2_jsonrpc_token, url_list, proxy=None):
    post_body = __build_post_body(aria2_jsonrpc_token, url_list)
    resp = requests.post(aria2_jsonrpc_url, json=post_body, proxies=req.build_proxies(proxy)).json()
    return bool((resp and ('result' in resp) and (resp['result'] == 'OK')))
