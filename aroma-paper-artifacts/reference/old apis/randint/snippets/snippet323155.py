import unittest
from random import randint
from ands.algorithms.crypto.caesar import MAX_MAPPED_INT, decrypt, decrypt_with_multiple_keys, encrypt, encrypt_with_multiple_keys
from tests.algorithms.crypto.util import find_max_char_ord_value, gen_rand_keys, generate_random_string


def test_multi_encrypt_decrypt_size_random_keys(self):
    keys = randint(3, 7)
    self.template_test_multi_keys(100, 1, keys)
