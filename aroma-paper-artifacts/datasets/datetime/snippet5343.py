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


def test_modified_file(self):
    'Test for modified file\n\n        :return:\n        '
    date_string = datetime.datetime.fromtimestamp(self.time_modifying).strftime('%d.%m.%Y %H:%M:%S')
    file_filter = Filter(modified_date=Constraint(date_string, cmp_func=Constraint.cmp_value_smaller_or_equal))
    files = file_filter.apply(directory=self.dir)
    len_files_before_modified_date = len(list(files))
    file_filter = Filter(modified_date=Constraint(date_string, cmp_func=Constraint.cmp_value_bigger))
    files = file_filter.apply(directory=self.dir)
    len_files_after_modified_date = len(list(files))
    self.assertTrue((len_files_after_modified_date == 1))
    self.assertTrue((len_files_before_modified_date > len_files_after_modified_date))
