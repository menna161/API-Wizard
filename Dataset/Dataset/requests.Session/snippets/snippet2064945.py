import unittest
from lxml import etree
from mock import MagicMock, patch
from rinse.client import SoapClient
from rinse.message import SoapMessage
from .utils import captured_stdout


def test_soap_action(self):
    'Test that SOAP action is passed on to SoapMessage.request().'
    msg = SoapMessage(etree.Element('test'))
    msg.request = MagicMock()
    with patch('requests.Session'):
        client = SoapClient('http://example.com')
        client(msg, 'testaction', build_response=(lambda r: r))
        msg.request.assert_called_once_with('http://example.com', 'testaction')
