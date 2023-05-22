import unittest
from lxml import etree
from mock import MagicMock, patch
from rinse.client import SoapClient
from rinse.message import SoapMessage
from .utils import captured_stdout


def test_timeout(self):
    msg = SoapMessage(etree.Element('test'))
    msg.request = MagicMock()
    client = SoapClient('http://example.com', timeout=1)
    self.assertEqual(client.timeout, 1)
    with patch('requests.Session'):
        client(msg, 'testaction', build_response=(lambda r: r))
        self.assertEqual(client._session.send.call_args[1]['timeout'], 1)
    with patch('requests.Session'):
        client(msg, 'testaction', build_response=(lambda r: r), timeout=2)
        self.assertEqual(client._session.send.call_args[1]['timeout'], 2)
    with patch('requests.Session'):
        client(msg, 'testaction', build_response=(lambda r: r), timeout=None)
        self.assertEqual(client._session.send.call_args[1]['timeout'], None)
