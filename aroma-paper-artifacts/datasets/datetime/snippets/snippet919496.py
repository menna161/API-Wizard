from datetime import datetime, timedelta
from starlette_auth import config
from starlette_auth.tables import User
from starlette_auth.tokens import PasswordResetTokenGenerator


def test_timeout(user):
    'The token is valid after n seconds, but no greater.'
    config.secret_key = 'some-secret-key'

    class Mocked(PasswordResetTokenGenerator):

        def __init__(self, now):
            self._now_val = now

        def _now(self):
            return self._now_val
    p0 = PasswordResetTokenGenerator()
    tk1 = p0.make_token(user)
    p1 = Mocked((datetime.utcnow() + timedelta(seconds=config.reset_pw_timeout)))
    assert p1.check_token(user, tk1)
    p2 = Mocked((datetime.utcnow() + timedelta(seconds=(config.reset_pw_timeout + 1))))
    assert (not p2.check_token(user, tk1))
    config.reset_pw_timeout = (60 * 60)
    p3 = Mocked((datetime.utcnow() + timedelta(seconds=config.reset_pw_timeout)))
    assert p3.check_token(user, tk1)
    p4 = Mocked((datetime.utcnow() + timedelta(seconds=(config.reset_pw_timeout + 1))))
    assert (not p4.check_token(user, tk1))
