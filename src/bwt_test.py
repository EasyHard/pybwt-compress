import bwt
import unittest
import random
from utils import *

class TestBWT(unittest.TestCase):

    def setUp(self):
        pass

    def test_sort_suffixes(self):
        seq = 'banana'
        indexes = bwt.sort_suffixes(seq)
        self.assertEqual([5, 3, 1, 0, 4, 2], indexes)

    def test_encode(self):
        seq = 'abraca'
        encode, I = bwt.encode(seq, indexes = [5, 0, 3, 1, 4, 2])
        self.assertEqual(list('caraab'), encode)
        self.assertEqual(I, 1)

    def test_decode(self):
        seq = 'caraab'
        decode = bwt.decode(seq, 1, True)
        self.assertEqual(list('abraca'), decode)

    def test_mix(self):
        seq = generator(16*1024)
        encode, I = bwt.encode(seq)
        decode = bwt.decode(encode, I, True)
        self.assertEqual(list(seq), decode)

if __name__ == '__main__':
    unittest.main()
