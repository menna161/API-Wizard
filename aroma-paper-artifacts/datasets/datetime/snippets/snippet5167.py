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


def get_token(self, expires_in=3600):
    now = datetime.utcnow()
    if (self.token and (self.token_expiration > (now + timedelta(seconds=60)))):
        return self.token
    self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
    self.token_expiration = (now + timedelta(seconds=expires_in))
    db.session.add(self)
    return self.token
