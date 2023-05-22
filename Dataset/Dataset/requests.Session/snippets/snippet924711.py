import json
import requests
from instabot import Bot
from unittest.mock import Mock, patch
from mock import Mock, patch
from uuid import UUID


@patch('instabot.API.load_uuid_and_cookie')
def test_login(self, load_cookie_mock):
    self.bot = Bot(save_logfile=False)
    load_cookie_mock.side_effect = Exception()

    def mockreturn(*args, **kwargs):
        r = Mock()
        r.status_code = 200
        r.text = '{"status": "ok"}'
        return r

    def mockreturn_login(*args, **kwargs):
        r = Mock()
        r.status_code = 200
        r.text = json.dumps({'logged_in_user': {'pk': self.USER_ID, 'username': self.USERNAME, 'full_name': self.FULLNAME}, 'status': 'ok'})
        return r
    with patch('requests.Session') as Session:
        instance = Session.return_value
        instance.get.return_value = mockreturn()
        instance.post.return_value = mockreturn_login()
        instance.cookies = requests.cookies.RequestsCookieJar()
        instance.cookies.update({'csrftoken': self.TOKEN, 'ds_user_id': self.USER_ID})
