from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def realtime_hotword():
    _params = {'containerid': '106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot'}
    _response = requests.get(url=_GET_INDEX, params=_params)
    if ((_response.status_code == 200) and (_response.json().get('ok') == 1)):
        return _response.json()
    raise WeiboApiException('weibo_comments request failed, url={0},params={1},response={2}'.format(_COMMENTS_HOTFLOW, _params, _response))
