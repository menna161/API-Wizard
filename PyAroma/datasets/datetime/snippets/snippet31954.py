import json
from datetime import datetime
from mock import Mock
from twisted.trial import unittest
from twisted.internet import defer
from twisted.python.failure import Failure
from twisted.web.client import ResponseDone
from txtorcon.router import Router, hexIdFromHash, hashFromHexId


def test_ctor(self):
    controller = object()
    router = Router(controller)
    router.update('foo', 'AHhuQ8zFQJdT8l42Axxc6m6kNwI', 'MAANkj30tnFvmoh7FsjVFr+cmcs', '2011-12-16 15:11:34', '77.183.225.114', '24051', '24052')
    self.assertEqual(router.id_hex, '$00786E43CCC5409753F25E36031C5CEA6EA43702')
    self.assertTrue(isinstance(router.modified, datetime))
    self.assertTrue(isinstance(router.modified, datetime))
    self.assertEqual(router.policy, '')
