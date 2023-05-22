import academictorrents as at
import unittest
import shutil
import sys, os, time
import datetime
from academictorrents import utils
from academictorrents import Torrent
from os.path import expanduser


def test_check_timestamp_two_weeks(self):
    ret = utils.timestamp_is_within_30_days((int(datetime.datetime.timestamp(datetime.datetime.now())) - (86400 * 14)))
    self.assertTrue(ret)
