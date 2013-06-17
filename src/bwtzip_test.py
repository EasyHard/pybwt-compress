import bwtzip
import unittest
import random
from StringIO import StringIO
from utils import *

class TestBWTZip(unittest.TestCase):

    def setUp(self):
        pass

    # def test_mix(self):
    #     seq = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4,5,5,5]
    #     random.shuffle(seq)
    #     from collections import Counter
    #     freqs = Counter(seq)
    #     expect = {1: '01', 2: '10', 3: '11', 4: '000', 5: '001'}
    #     coding, root = huff.generate_coding(freqs)
    #     self.assertDictEqual(expect, coding)

    #     encode = huff.encode(seq, coding)
    #     print encode
    #     decode = huff.decode(''.join(encode), root)
    #     self.assertEqual(seq, decode)

    def test_freqs_dump_load(self):
        seq = generator(16*1024, chars = string.digits)
        seq = [int(x) for x in seq]
        from collections import Counter
        freqs = Counter(seq)
        f = StringIO()
        bwtzip.dump_freqs(f, freqs)
        newf = StringIO(f.getvalue())
        newfreqs = bwtzip.load_freqs(newf)
        self.assertDictEqual(freqs, newfreqs)

    def test_bwtzip(self):
        f = open("bwtzip.py")
        compf = StringIO()
        bwtzip.compress(f, compf)
        rcompf = StringIO(compf.getvalue())
        newf = StringIO()
        bwtzip.decompress(compf = rcompf, f = newf)
        self.assertEqual(newf.getvalue(), open("bwtzip.py").read())
        print "radio = %r" % (float(compf.tell())/f.tell())

if __name__ == '__main__':
    unittest.main()
