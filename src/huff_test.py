import huff
import unittest
import random
from utils import *

class TestHuff(unittest.TestCase):

    def setUp(self):
        pass

    def test_mix(self):
        seq = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,5,5,5]
        random.shuffle(seq)
        from collections import Counter
        freqs = Counter(seq)
        expect = {1: '10', 2: '01', 3: '11', 4: '001', 5: '000'}
        coding, root = huff.generate_coding(freqs)
        self.assertDictEqual(expect, coding)

        encode = huff.encode(seq, coding)
        decode = huff.decode(''.join(encode), root)
        self.assertEqual(seq, decode)

    def test_ed(self):
        seq = generator(16*1024)
        from collections import Counter
        freqs = Counter(seq)
        coding, root = huff.generate_coding(freqs)
        encode = huff.encode(seq, coding)
        decode = huff.decode(''.join(encode), root)
        self.assertEqual(list(seq), decode)

    def test_same(self):
        seq = [0]*16
        from collections import Counter
        freqs = Counter(seq)
        coding, root = huff.generate_coding(freqs)
        encode = huff.encode(seq, coding)
        decode = huff.decode(''.join(encode), root)
        self.assertEqual(list(seq), decode)

if __name__ == '__main__':
    unittest.main()
