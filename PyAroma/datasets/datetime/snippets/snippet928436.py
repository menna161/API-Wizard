from twisted.trial import unittest
from autobahntestsuite import wamptestee
import types
import datetime


def testEcho(self):
    '\n        The echo service should echo received parameters correctly,\n        regardless of their type.\n        '
    for val in ['Hallo', 5, (- 1000), datetime.datetime.now(), True]:
        self.assertEquals(self.echo_service.echo(val), val)
