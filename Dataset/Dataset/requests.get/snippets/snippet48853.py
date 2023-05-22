from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def weibo_tweets(containerid: str, page: int) -> Response:
    "\n    get person weibo tweets which from contaninerid in page,\n    this api is like 'https://m.weibo.cn/container/getIndex?containerid=<containerid>&page=<page>'\n    >>> from weibo_base import  weibo_tweets\n    >>> _response = weibo_tweets(contaierid='1076031843242321',page=1)\n    :param containerid:\n    :param page: page\n    :return:\n    "
    _params = {'containerid': containerid, 'page': page}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if ((_response.status_code == 200) and (_response.json().get('ok') == 1)):
        return _response.json()
    raise WeiboApiException('weibo_tweets request failed, url={0},params={1},response={2}'.format(_GET_INDEX, _params, (_response if (_response is None) else _response.text)))
