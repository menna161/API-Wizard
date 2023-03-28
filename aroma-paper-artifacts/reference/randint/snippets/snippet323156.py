import unittest
from random import randint
from ands.algorithms.crypto.caesar import MAX_MAPPED_INT, decrypt, decrypt_with_multiple_keys, encrypt, encrypt_with_multiple_keys
from tests.algorithms.crypto.util import find_max_char_ord_value, gen_rand_keys, generate_random_string


def test_multi_encrypt_decrypt_random(self):
    'Random number of iterations, random length of message\n        and random number of keys.'
    it = randint(3, 13)
    size = randint(10, 1000)
    keys = randint(3, 11)
    self.template_test_multi_keys(it, size, keys)
