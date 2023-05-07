import datetime
import ipaddress
from mock import patch
from twisted.trial import unittest
from twisted.internet import defer
from twisted.python.failure import Failure
from zope.interface import implementer
from txtorcon import Circuit
from txtorcon import Stream
from txtorcon import TorControlProtocol
from txtorcon import TorState
from txtorcon import Router
from txtorcon.router import hexIdFromHash
from txtorcon.circuit import TorCircuitEndpoint, _get_circuit_attacher
from txtorcon.interface import IRouterContainer
from txtorcon.interface import ICircuitListener
from txtorcon.interface import ICircuitContainer
from txtorcon.interface import CircuitListenerMixin
from txtorcon.interface import ITorControlProtocol
from mock import Mock
from datetime import datetime
from zope.interface.verify import verifyObject


def test_age(self):
    '\n        make sure age does something sensible at least once.\n        '
    tor = FakeTorController()
    circuit = Circuit(tor)
    now = datetime.datetime.now()
    update = ('1 LAUNCHED PURPOSE=GENERAL TIME_CREATED=%s' % now.strftime('%Y-%m-%dT%H:%M:%S'))
    circuit.update(update.split())
    diff = circuit.age(now=now)
    self.assertEqual(diff, 0)
    self.assertTrue((circuit.time_created is not None))
