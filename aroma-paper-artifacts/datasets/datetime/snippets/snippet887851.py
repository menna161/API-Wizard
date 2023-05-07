import datetime
import io
import sys
import time
import unittest
from xml.sax import saxutils


def run(self, test):
    'Run the given test case or test suite.'
    result = _TestResult(self.verbosity)
    test(result)
    self.stopTime = datetime.datetime.now()
    self.generateReport(test, result)
    print(sys.stderr, ('\nTime Elapsed: %s' % (self.stopTime - self.startTime)))
    return result
