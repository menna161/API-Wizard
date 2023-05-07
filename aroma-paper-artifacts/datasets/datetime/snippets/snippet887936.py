import jwt
from datetime import datetime, timedelta
from flask import current_app, request, session
from functools import wraps
from app.utils.code import ResponseCode
from app.utils.util import ResMsg


@classmethod
def generate_access_token(cls, user_id, algorithm: str='HS256', exp: float=2):
    '\n        生成access_token\n        :param user_id:自定义部分\n        :param algorithm:加密算法\n        :param exp:过期时间\n        :return:\n        '
    key = current_app.config.get('SECRET_KEY', cls.key)
    now = datetime.utcnow()
    exp_datetime = (now + timedelta(hours=exp))
    access_payload = {'exp': exp_datetime, 'flag': 0, 'iat': now, 'iss': 'qin', 'user_id': user_id}
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token
