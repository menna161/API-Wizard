from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def weibo_getIndex(uid_value: str) -> Response:
    "\n    get personal summary info which request by uid, and uid is got by 'search_by_name'\n    this api is like 'https://m.weibo.cn/api/container/getIndex?type=uid&value=<uid_value sample as 1843242321>'\n\n    >>> from weibo_base import  weibo_getIndex\n    >>> _response = weibo_getIndex('1843242321')\n    :param uid_value:\n    :return:\n    "
    _params = {'type': 'uid', 'value': uid_value}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if (_response.status_code == 200):
        return _response.json()
    return None
