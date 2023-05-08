import unittest
import sys
import afterhours.utils as utils
import afterhours.utils as utils
import datetime


def format_date(self):
    import datetime
    res = utils.formatoutput(('12:07:03 PM', '12', '2', '2018'), outtype='date')
    self.assertIsInstance(res, datetime.datetime, 'formatoutput unexecpted formatting did not return datetime\n                              \nreturned: {}'.format(type(res)))
