import json
import requests
from instabot import Bot
from unittest.mock import Mock, patch
from mock import Mock, patch
from uuid import UUID


def prepare_api(self, bot):
    bot.api.is_logged_in = True
    bot.api.session = requests.Session()
    cookies = Mock()
    cookies.return_value = {'csrftoken': self.TOKEN, 'ds_user_id': self.USER_ID}
    bot.api.session.cookies.get_dict = cookies
    bot.api.set_user(self.USERNAME, self.PASSWORD)
