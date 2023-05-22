from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def weibo_second(containerid: str, page: int) -> Response:
    '\n    https://m.weibo.cn/api/container/getSecond\n    :param containerid:\n    :param page:\n    :return:\n    '
    _params = {'containerid': containerid, 'page': page}
    _response = requests.get(url=_GET_SECOND, params=_params)
    if ((_response.status_code == 200) and (_response.json().get('ok') == 1)):
        return _response.json()
    raise WeiboApiException('weibo_second request failed, url={0},params={1},response={2}'.format(_GET_SECOND, _params, _response))
