def sort_suffixes(seq):
    """
    Sorting all suffixes of seq and return a index list.
    There are several algorithms to improve the sorting performance,
    like suffix tree or SA-IS. But currently a naive approach is
    implemented for simplity.
    """
    seq = list(seq)
    return sorted(range(len(seq)),
                  key = lambda x:seq[x:])

def encode(seq, indexes = None):
    seq = list(seq)
    if indexes == None:
        seq.append('')
        indexes = sort_suffixes(seq)
    L = []
    for index in indexes:
        L.append(seq[index-1])
    return L, indexes.index(0)

import bisect
def decode(L, I, reverse = False):
    L = list(L)
    F = sorted(L)
    T = []
    times = {}
    for x in L:
        last, start = times.get(x, (0,0))
        k = last + 1
        index = bisect.bisect_left(F, x, start)
        times[x] = (k, index+1)
        T.append(index)
    output = []
    curr = I
    for i in xrange(len(L)):
        output.append(L[curr])
        curr = T[curr]
    if reverse:
        output.reverse()
    if output[-1] == '':
        output = output[:-1]
    return output

