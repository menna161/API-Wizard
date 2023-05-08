import unittest
from random import randint
from ands.algorithms.crypto.one_time_pad import decrypt, encrypt
from tests.algorithms.crypto.util import generate_random_string


def test_random_size(self):
    it = randint(3, 11)
    size = randint(10, 1000)
    self.template_test(it, size)
