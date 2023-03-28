import unittest
from random import randint
from ands.algorithms.crypto.caesar import MAX_MAPPED_INT, decrypt, decrypt_with_multiple_keys, encrypt, encrypt_with_multiple_keys
from tests.algorithms.crypto.util import find_max_char_ord_value, gen_rand_keys, generate_random_string


def template_test_one_key(self, n, size):
    'n is the number of iterations.\n        size is the size of the message.'
    for _ in range(n):
        m = generate_random_string(size)
        key = randint(1, (MAX_MAPPED_INT - find_max_char_ord_value(m)))
        cipher = encrypt(m, key)
        o = decrypt(cipher, key)
        self.assertEqual(m, o)
