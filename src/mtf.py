"""
Move-to-front encoder/decoder
"""

def move_to_front(l, index):
    """
    Return a new list that move l[index] to the front.
    """
    return [l[index]] + l[:index] + l[index+1:]

def encode(alphabet, seq, needsort=False):
    """
    Encoder of Move-to-front algorithm.

    alphabet: string/chars of symbols
    seq: list of string/chars to be encoded.
    needsort: whether alphabet needs sort first.

    Return: list ofencoded strings/chars
    """
    output_seq = []
    if needsort:
        alphabet = sorted(alphabet)
    seq = list(seq)
    alphabet = list(alphabet)
    for x in seq:
        index = alphabet.index(x)
        output_seq.append(index)
        alphabet = move_to_front(alphabet, index)
    return output_seq

def decode(alphabet, seq, needsort=False):
    """
    Decoder. Similar with encode()
    """
    output_seq = []
    if needsort:
        alphabet = sorted(alphabet)
    seq = list(seq)
    alphabet = list(alphabet)
    for x in seq:
        output_seq.append(alphabet[x])
        alphabet = move_to_front(alphabet, x)
    return output_seq
