from array import array
import random
import unittest
from .. import cobs as cobs


def test_random(self):
    try:
        for _test_num in range(self.NUM_TESTS):
            length = random.randint(0, self.MAX_LENGTH)
            test_string = bytes((random.randint(0, 255) for x in range(length)))
            encoded = cobs.encode(test_string)
            self.assertTrue((b'\x00' not in encoded), ('encoding contains zero byte(s):\noriginal: %s\nencoded: %s' % (repr(test_string), repr(encoded))))
            self.assertTrue((len(encoded) <= ((len(test_string) + 1) + (len(test_string) // 254))), ('encoding too big:\noriginal: %s\nencoded: %s' % (repr(test_string), repr(encoded))))
            decoded = cobs.decode(encoded)
            self.assertEqual(decoded, test_string, ('encoding and decoding random data failed:\noriginal: %s\ndecoded: %s' % (repr(test_string), repr(decoded))))
    except KeyboardInterrupt:
        pass
