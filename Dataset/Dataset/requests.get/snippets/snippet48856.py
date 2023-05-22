from typing import Optional
from weibo_base.weibo_util import RequestProxy, WeiboApiException


def weibo_comments(id: str, mid: str) -> Response:
    '\n    https://m.weibo.cn/comments/hotflow?id=4257059677028285&mid=4257059677028285\n    get comments from userId and mid\n    :param id:          userId\n    :param mid:         mid\n    :return:\n    '
    _params = {'id': id, 'mid': mid}
    _response = requests.get(url=_COMMENTS_HOTFLOW, params=_params)
    if ((_response.status_code == 200) and (_response.json().get('ok') == 1)):
        return _response.json()
    raise WeiboApiException('weibo_comments request failed, url={0},params={1},response={2}'.format(_COMMENTS_HOTFLOW, _params, _response))
