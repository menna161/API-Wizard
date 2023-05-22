import functools
import json
import random
import re
import string
from http.client import HTTPConnection
from urllib.parse import parse_qsl
import urllib3
from evernotebot.storage import Storage
from evernotebot.util.asgi import AsgiApplication
from tests.telegram.models import Chat, User


def api_add_user(self, request):
    data = request.json()
    user_id = data.get('user_id')
    if (not user_id):
        while True:
            user_id = random.randint(1, 1000000)
            if (not self.users.get(user_id)):
                break
    elif self.users.get(user_id):
        raise Exception(f'User `{user_id}` already exists')
    user_data = {'id': user_id, 'user_id': user_id, 'first_name': data.get('first_name', f'Client {user_id}'), 'last_name': data.get('last_name', ''), 'username': data.get('username', f'user_{user_id}'), 'language_code': data.get('language_code', 'en')}
    if data.get('is_bot'):
        random_char = functools.partial(random.choice, string.ascii_letters)
        token = (data.get('token') or ''.join([random_char() for _ in range(32)]))
        user_data.update({'bot_name': data['bot_name'], 'token': token, 'is_bot': True})
    self.users.create(user_data)
    return user_data
