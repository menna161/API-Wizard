import datetime
import io
import unittest
from unittest import mock
from aranet4 import client
from aranet4 import aranetctl


def test_parse_args4(self):
    expected = base_args.copy()
    expected['records'] = True
    expected['start'] = datetime.datetime(2022, 2, 14, 15, 16)
    expected['end'] = datetime.datetime(2022, 2, 17, 18, 19)
    args = aranetctl.parse_args('11:22:33:44:55:66 -r -s 2022-02-14T15:16 -e 2022-02-17T18:19'.split())
    self.assertDictEqual(expected, args.__dict__)
