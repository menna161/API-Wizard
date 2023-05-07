import datetime
import math
import os
import re
import shutil
import unittest
import uuid
from stat import ST_MTIME, ST_ATIME
from time import time, sleep
from saucenao.files.constraint import Constraint
from saucenao.files.filter import Filter


def test_creation_date(self):
    'Test for filtering after creation date\n\n        :return:\n        '
    date_string = datetime.datetime.fromtimestamp(self.time_modifying).strftime('%d.%m.%Y %H:%M')
    file_filter = Filter(creation_date=Constraint(date_string, cmp_func=Constraint.cmp_value_bigger_or_equal))
    files = file_filter.apply(directory=self.dir)
    self.assertEqual(len(list(files)), 4)
    file_filter = Filter(creation_date=Constraint(date_string, cmp_func=Constraint.cmp_value_smaller))
    files = file_filter.apply(directory=self.dir)
    self.assertEqual(len(list(files)), 0)
