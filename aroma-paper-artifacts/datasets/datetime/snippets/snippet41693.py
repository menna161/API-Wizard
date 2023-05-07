import unittest
from datetime import datetime, timezone
from email import utils
from kiss_headers import Allow, ContentDisposition, ContentLength, ContentType, CrossOriginResourcePolicy, CustomHeader, Date, From, ReferrerPolicy, SetCookie


def test_set_cookie(self):
    dt = datetime.now()
    self.assertEqual(repr(SetCookie('MACHINE_IDENTIFIANT', 'ABCDEFGHI', expires=dt)), 'Set-Cookie: MACHINE_IDENTIFIANT="ABCDEFGHI"; expires="{dt}"; HttpOnly'.format(dt=utils.format_datetime(dt.astimezone(timezone.utc), usegmt=True)))
