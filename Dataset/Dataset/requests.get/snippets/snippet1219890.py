import mock
from lxml import etree
from unittest import TestCase
from .address import Address
from .usps import USPSApi, USPSApiError


@mock.patch('requests.get')
def test_send_request_error(self, requests_mock):
    requests_mock.return_value.content = b'<Error><Description>Test Error</Description></Error>'
    with self.assertRaises(USPSApiError):
        self.usps.send_request('tracking', etree.Element('asdf'))
