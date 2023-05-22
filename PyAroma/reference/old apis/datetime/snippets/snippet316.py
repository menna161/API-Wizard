from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings


def jwt_payload_handler(user):
    ' Custom payload handler\n    Token encrypts the dictionary returned by this function, and can be\n    decoded by rest_framework_jwt.utils.jwt_decode_handler\n    '
    return {'userId': user.pk, 'username': user.username, 'email': user.email, 'isStaff': user.is_staff, 'exp': (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA), 'orig_iat': timegm(datetime.utcnow().utctimetuple())}
