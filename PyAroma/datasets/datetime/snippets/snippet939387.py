import hashlib
import hmac
import datetime
from uuid import uuid4
import jwt
from chalice import UnauthorizedError


def get_jwt_token(username, password, record):
    actual = hashlib.pbkdf2_hmac(record['hash'], password, record['salt'].value, record['rounds'])
    expected = record['hashed'].value
    if hmac.compare_digest(actual, expected):
        now = datetime.datetime.utcnow()
        unique_id = str(uuid4())
        payload = {'sub': username, 'iat': now, 'nbf': now, 'jti': unique_id}
        return jwt.encode(payload, _SECRET, algorithm='HS256')
    raise UnauthorizedError('Invalid password')
