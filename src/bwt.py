def sort_suffixes(seq):
    """
    Sorting all suffixes of seq and return a index list.
    There are several algorithms to improve the sorting performance,
    like suffix tree or SA-IS. But currently a n*logn*logn approach is
    implemented for simplity.
    """
    seq = list(seq)
    l = []
    for i in xrange(len(seq)):
        l.append([seq[i], i, None])
    sorted_l = sorted(l, key = lambda x: x[0])
    rank = 1
    for i in xrange(len(sorted_l)):
        if i != 0 and sorted_l[i-1][0] != sorted_l[i][0]:
            rank = rank + 1
        l[sorted_l[i][1]][2] = rank
    # print "l:"
    # print l
    currlen = 1
    lenseq = len(seq)
    while currlen < len(seq):
        for i in xrange(len(l)):
            nextrank = 0
            if i+currlen < lenseq:
                nextrank = l[i+currlen][2]
            l[i][2] = (l[i][2], nextrank)
        # print "l:"
        # print l
        sorted_l = sorted(l, key = lambda x: x[2])
        # print "sorted l:"
        # print sorted_l

        rank = 1
        newranks = []
        for i in xrange(len(sorted_l)):
            if i != 0 and sorted_l[i-1][2] != sorted_l[i][2]:
                rank = rank + 1
            newranks.append(rank)
        # print "newranks:"
        # print newranks
        for i in xrange(lenseq):
            l[sorted_l[i][1]][2] = newranks[i]
        # print "l:"
        # print l
        currlen = currlen * 2
    return [x[1] for x in sorted_l]

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
