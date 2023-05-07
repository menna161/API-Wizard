import jwt
from uuid import uuid4
from flask import current_app
import datetime


@staticmethod
def _create_basic_token_data(identity, token_type):
    uid = str(uuid4())
    now = datetime.datetime.utcnow()
    token_data = {'type': token_type, 'iat': now, 'nbf': now, 'jti': uid, current_app.config['JWT_IDENTITY_CLAIM']: identity}
    if (token_type == 'refresh'):
        exp = current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        if isinstance(exp, int):
            exp = datetime.timedelta(days=exp)
    else:
        exp = current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        if isinstance(exp, int):
            exp = datetime.timedelta(minutes=exp)
    token_data.update({'exp': (now + exp)})
    return token_data
