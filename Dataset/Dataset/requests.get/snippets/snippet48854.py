from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def weibo_containerid(containerid: str, page: int) -> Response:
    '\n\n    :param containerid:\n    :param page:\n    :return:\n    '
    _params = {'containerid': containerid, 'page': page}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if ((_response.status_code == 200) and (_response.json().get('ok') == 1)):
        return _response.json()
    raise WeiboApiException('weibo_containerid request failed, url={0},params={1},response={2}'.format(_GET_INDEX, _params, _response))
