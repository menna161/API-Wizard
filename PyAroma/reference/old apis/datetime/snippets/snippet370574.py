import datetime
import sys
import io
import time
import unittest
from xml.sax import saxutils


def run(self, test):
    'Run the given test case or test suite.'
    result = _TestResult(self.verbosity)
    test(result)
    self.stopTime = datetime.datetime.now()
    self.generateReport(test, result)
    print(('\nTime Elapsed: %s' % (self.stopTime - self.startTime)), file=sys.stderr)
    return result
