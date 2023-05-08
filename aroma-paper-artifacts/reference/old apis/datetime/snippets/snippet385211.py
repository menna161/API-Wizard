from __future__ import print_function
import datetime
from unittest import TestCase
from boto.regioninfo import RegionInfo
from mock import Mock, patch
from monocyte import Monocyte
from monocyte.handler import Resource, Handler
from monocyte.cli import apply_default_config


def fetch_unwanted_resources(self):
    return [Resource(Mock(), 'ec2 instance', '123456789', datetime.datetime.now(), 'us'), Resource(Mock(), 'ec2 volume', '33123456789', datetime.datetime.now(), 'us')]
