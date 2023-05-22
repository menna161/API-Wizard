import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import redis
import rq
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


@staticmethod
def check_token(token):
    user = User.query.filter_by(token=token).first()
    if ((user is None) or (user.token_expiration < datetime.utcnow())):
        return None
    return user
