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


def new_messages(self):
    last_read_time = (self.last_message_read_time or datetime(1900, 1, 1))
    return Message.query.filter_by(recipient=self).filter((Message.timestamp > last_read_time)).count()
