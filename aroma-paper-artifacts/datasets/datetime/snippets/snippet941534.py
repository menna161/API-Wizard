import jwt
from uuid import uuid4
from flask import current_app
import datetime


@staticmethod
def _set_default__configuration_options(app):
    '\n        Sets the default configuration options used by this extension\n        '
    app.config.setdefault('JWT_TOKEN_ARGUMENT_NAME', 'token')
    app.config.setdefault('JWT_REFRESH_TOKEN_ARGUMENT_NAME', 'refresh_token')
    app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', datetime.timedelta(minutes=15))
    app.config.setdefault('JWT_SECRET_KEY', app.config.get('SECRET_KEY'))
    app.config.setdefault('JWT_REFRESH_TOKEN_EXPIRES', datetime.timedelta(days=30))
    app.config.setdefault('JWT_IDENTITY_CLAIM', 'identity')
    app.config.setdefault('JWT_USER_CLAIMS', 'user_claims')
    app.config.setdefault('JWT_HEADER_NAME', 'Authorization')
    app.config.setdefault('JWT_HEADER_TOKEN_PREFIX', 'bearer')
