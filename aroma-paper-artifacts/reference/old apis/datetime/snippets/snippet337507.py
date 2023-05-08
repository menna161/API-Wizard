from datetime import datetime
from pymongo import MongoClient
from appkernel.configuration import config
from tests.utils import User, create_and_save_a_user, Task


def test_unix_time_marshaller():
    user = create_and_save_a_user('test user', 'test password', 'test description')
    user.last_login = datetime.now()
    user.finalise_and_validate()
    print('\n\n')
    user_json = user.dumps(pretty_print=True)
    print(user_json)
    assert isinstance(User.to_dict(user).get('last_login'), float)
    reloaded_user = User.loads(user_json)
    print(str(reloaded_user))
    assert isinstance(reloaded_user.last_login, datetime)
