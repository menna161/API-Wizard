import unittest
from random import randint
from ands.algorithms.dac.find_peak import find_peak, find_peak_linearly


def test_find_peak_all_elements_are_equal(self):
    a = ([randint((- 100), 100)] * 10)
    self.assertNotEqual(find_peak(a), (- 1))
    self.assertNotEqual(find_peak_linearly(a), (- 1))
