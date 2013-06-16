import mtf
import unittest
import string
import random
from utils import *

def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in xrange(size))

class TestMTF(unittest.TestCase):

    def setUp(self):
        pass

    def test_encode(self):
        l = mtf.encode('abcr', 'caraab')
        self.assertEqual(l, [2, 1, 3, 1, 0, 3])

    def test_decode(self):
        l = mtf.decode('abcr', [2, 1, 3, 1, 0, 3])
        self.assertEqual(l, list('caraab'))

    def test_both(self):
        for x in xrange(10):
            chars = string.ascii_uppercase + string.digits
            seq = generator(1024*16, chars)
            encode_seq = mtf.encode(chars, seq)
            decode_seq = mtf.decode(chars, encode_seq)
            self.assertEqual(decode_seq, list(seq))

if __name__ == '__main__':
    unittest.main()
