from __future__ import print_function
import datetime
from unittest import TestCase
from boto.regioninfo import RegionInfo
from mock import Mock, patch
from monocyte import Monocyte
from monocyte.handler import Resource, Handler
from monocyte.cli import apply_default_config


def test_handle_service(self):
    handler = Mock()
    handler.fetch_unwanted_resources.return_value = [Resource('foo', 'test_type', 'test_id', datetime.datetime.now(), 'test_region')]
    handler.to_string.return_value = 'test handler'
    self.monocyte.handle_service(handler)
    self.logger_mock.getLogger.return_value.warning.assert_called_with(REGION_NOT_ALLOWED)
