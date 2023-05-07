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


def api_create_chats(self, user_id: int, request):
    user_id = int(user_id)
    for user_data in self.users.get_all():
        if (user_id == user_data['id']):
            continue
        chat_id = random.randint(1, 1000000)
        self.chats.create({'id': chat_id, 'chat_id': chat_id, 'members': [user_id, int(user_data['id'])]})
    return {'chats': list(self.chats.get_all())}
