#!/usr/bin/python2
import bwt, mtf, huff
from bitarray import bitarray # For handling bits
from collections import Counter
import struct
import cPickle

BLOCK_SIZE=8*1024

def dump_freqs(f, freqs):
    f.write(struct.pack(">H", len(freqs)))
    for k,v in freqs.items():
        f.write(struct.pack(">2H", k, v))

def load_freqs(f):
    freqs_len, = struct.unpack(">H", f.read(2))
    freqs = {}
    for i in xrange(freqs_len):
        k, v, = struct.unpack(">2H", f.read(4))
        freqs[k] = v
    return freqs

def compress(f, compf, block = None):
    """
    Compress a file by bwt-mtf-huff processes.
    f: a file-like object, content for compressing
    compf: compression result
    """
    # craete alphabet for move-to-front
    content = f.read()
    alphabet_set = set(content)
    alphabet = [''] + list(alphabet_set)
    # dump alphabet
    cPickle.dump(alphabet, compf, 2)
    content = None
    f.seek(0)
    count = 0
    while True:
        data = f.read(BLOCK_SIZE)
        if data == '':
            break
        if block == None or block == count:
            print "block %r:" % count
            bwt_encode, I = bwt.encode(data)
            mtf_encode = mtf.encode(alphabet, bwt_encode)
            # create Huffman tree
            freqs = Counter(mtf_encode)
            if block:
                print freqs
            coding, root = huff.generate_coding(freqs)
            if block:
                print coding
            # encoding
            huff_encode = ''.join(huff.encode(mtf_encode, coding))
            #print "huff_encode:\n%r" % huff_encode
            nbits = len(huff_encode)
            huff_bytes = bitarray(huff_encode).tobytes()

            compf.write(struct.pack(">2I", nbits, I))
            dump_freqs(compf, freqs)
            compf.write(huff_bytes)

            print "nbits = %r, I = %r, length = %r" % (nbits, I, len(data))
        count = count + 1

def decompress(compf, f):
    """
    Decompress a file.
    """
    # read alphabet
    alphabet = cPickle.load(compf)
    print "alphabet:\n%r" % alphabet
    count = 0
    while True:
        header = compf.read(8)
        if header == '':
            break
        print "block %r:" % count
        nbits, I = struct.unpack('>2I', header)
        freqs = load_freqs(compf)
        #print freqs
        nbyte = (nbits+7) / 8
        t = bitarray()
        t.frombytes(compf.read(nbyte))
        huff_encode = t.to01()[:nbits]
        #print "huff_encode:\n%r" % huff_encode
        coding, root = huff.generate_coding(freqs)
        #print "coding:\n%r" % coding
        huff_decode = huff.decode(huff_encode, root)
        mtf_decode = mtf.decode(alphabet, huff_decode)
        bwt_decode = bwt.decode(mtf_decode, I, reverse = True)
        content = ''.join(bwt_decode)
        f.write(content)
        print "nbits = %r, I = %r, length = %r" % (nbits, I, len(content))
        count = count + 1

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'c':
        f = open(sys.argv[2], "r")
        compf = open(sys.argv[2]+".bwt", "w")
        compress(f, compf)
        fsize = f.tell()
        compfsize = compf.tell()
        f.close()
        compf.close()
        print "Before compress: %r bytes." % fsize
        print "After  compress: %r bytes." % compfsize
        print "radio: %f" % (float(compfsize) / fsize)
    if sys.argv[1] == 'd':
        compf = open(sys.argv[2], "r")
        f = open(sys.argv[3], "w")
        decompress(compf = compf, f = f)
        compf.close()
        f.close()
