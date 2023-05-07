from array import array
import random
import unittest
import cobsr_wrapper as cobsr


def test_random(self):
    try:
        for _test_num in xrange(self.NUM_TESTS):
            length = random.randint(0, self.MAX_LENGTH)
            test_string = ''.join((chr(random.randint(0, 255)) for x in xrange(length)))
            encoded = cobsr.encode(test_string)
            self.assertTrue(('\x00' not in encoded), ('encoding contains zero byte(s):\noriginal: %s\nencoded: %s' % (repr(test_string), repr(encoded))))
            self.assertTrue((len(encoded) <= ((len(test_string) + 1) + (len(test_string) // 254))), ('encoding too big:\noriginal: %s\nencoded: %s' % (repr(test_string), repr(encoded))))
            decoded = cobsr.decode(encoded)
            self.assertEqual(decoded, test_string, ('encoding and decoding random data failed:\noriginal: %s\ndecoded: %s' % (repr(test_string), repr(decoded))))
    except KeyboardInterrupt:
        pass
