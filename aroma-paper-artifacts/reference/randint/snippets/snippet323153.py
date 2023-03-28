import unittest
from random import randint
from ands.algorithms.crypto.caesar import MAX_MAPPED_INT, decrypt, decrypt_with_multiple_keys, encrypt, encrypt_with_multiple_keys
from tests.algorithms.crypto.util import find_max_char_ord_value, gen_rand_keys, generate_random_string


def test_encrypt_and_decrypt_random_size(self):
    it = randint(3, 13)
    size = randint(10, 1000)
    self.template_test_one_key(it, size)
