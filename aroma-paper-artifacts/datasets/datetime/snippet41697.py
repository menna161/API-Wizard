import unittest
from datetime import datetime, timezone
from email import utils
from kiss_headers import Allow, ContentDisposition, ContentLength, ContentType, CrossOriginResourcePolicy, CustomHeader, Date, From, ReferrerPolicy, SetCookie


def test_verify_always_gmt(self):
    self.assertTrue(repr(Date(datetime.now())).endswith('GMT'))
