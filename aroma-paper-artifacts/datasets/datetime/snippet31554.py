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


def test_no_age_yet(self):
    "\n        make sure age doesn't explode if there's no TIME_CREATED flag.\n        "
    tor = FakeTorController()
    circuit = Circuit(tor)
    now = datetime.datetime.now()
    circuit.update('1 LAUNCHED PURPOSE=GENERAL'.split())
    self.assertTrue((circuit.time_created is None))
    diff = circuit.age(now=now)
    self.assertEqual(diff, None)
