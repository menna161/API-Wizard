import jwt
from datetime import datetime, timedelta
from flask import current_app, request, session
from functools import wraps
from app.utils.code import ResponseCode
from app.utils.util import ResMsg


@classmethod
def generate_refresh_token(cls, user_id, algorithm: str='HS256', fresh: float=30):
    '\n        生成refresh_token\n\n        :param user_id:自定义部分\n        :param algorithm:加密算法\n        :param fresh:过期时间\n        :return:\n        '
    key = current_app.config.get('SECRET_KEY', cls.key)
    now = datetime.utcnow()
    exp_datetime = (now + timedelta(days=fresh))
    refresh_payload = {'exp': exp_datetime, 'flag': 1, 'iat': now, 'iss': 'qin', 'user_id': user_id}
    refresh_token = jwt.encode(refresh_payload, key, algorithm=algorithm)
    return refresh_token
