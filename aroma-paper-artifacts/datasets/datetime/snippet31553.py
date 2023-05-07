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


@patch('txtorcon.circuit.datetime')
def test_age_default(self, fake_datetime):
    '\n        age() w/ defaults works properly\n        '
    from datetime import datetime
    now = datetime.fromtimestamp(60.0)
    fake_datetime.return_value = now
    fake_datetime.utcnow = Mock(return_value=now)
    tor = FakeTorController()
    circuit = Circuit(tor)
    circuit._time_created = datetime.fromtimestamp(0.0)
    self.assertEqual(circuit.age(), 60)
    self.assertTrue((circuit.time_created is not None))
