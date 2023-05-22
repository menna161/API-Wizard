import mock
from lxml import etree
from unittest import TestCase
from .address import Address
from .usps import USPSApi, USPSApiError


@mock.patch('requests.get')
def test_send_request_valid(self, requests_mock):
    requests_mock.return_value.content = b'<Valid>test</Valid>'
    response = self.usps.send_request('tracking', etree.Element('asdf'))
    self.assertEqual(response, {'Valid': 'test'})
