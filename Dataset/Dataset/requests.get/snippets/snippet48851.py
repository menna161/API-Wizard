from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def search_by_name(name: str) -> Response:
    "get summary info which searched by name,\n     this api is like 'https://m.weibo.cn/api/container/getIndex?queryVal=<name sample as Helixcs>&containerid=100103type%3D3%26q%3D<name sample as Helixcs>'\n\n    >>> from weibo_base import search_by_name\n    >>> _response = search_by_name('Helixcs')\n     :param name: nick name which you want to search\n     :return json string including summary info\n    "
    _params = {'queryVal': name, 'containerid': ('100103type%3D3%26q%3D' + name)}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if (_response.status_code == 200):
        return _response.json()
    return None
