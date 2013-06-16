"""
Implement of Huffman encoder/decoder
"""

class TreeNode(object):
    """
    Node of Huffman tree.
    """
    left = None # Left for 0
    right = None # Right for 1
    freq = None
    symbol = None
    rank = 0
    def __init__(self, freq = 0, symbol = None, left = None, right = None,
                 rank = 0):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.rank = rank

    def __le__(self, other):
        if self.freq != other.freq:
            return self.freq <= other.freq
        else:
            return self.rank <= other.rank

    def find_symbol(self, code, depth = 0):
        if self.symbol != None:
            return self.symbol, depth
        if code[0] == '0':
            return self.left.find_symbol(code[1:], depth+1)
        elif code[0] == '1':
            return self.right.find_symbol(code[1:], depth+1)
        else:
            raise TypeError("code: "+code+" should be 0-1 string")

    def __str__(self):
        return "(%r, %r)" % (self.symbol, self.freq)

def generate_coding(freqs):
    """
    Return a dict of coding mapping and a prefix-code Huffman tree
    for freqs
    """
    if len(freqs) == 0:
        return None, None
    if len(freqs) == 1:
        k, v = freqs.items()[0]
        coding = {k:'0'}
        left = TreeNode(freq=v, symbol = k)
        root = TreeNode(left=left)
        return coding, root
    freqs = dict(freqs)
    import heapq
    h = []
    rank = 0
    items = sorted(freqs.items(), key=lambda x:x[0])
    #print items
    for x, v in items:
        node = TreeNode(freq = v, symbol = x, rank = rank)
        rank = rank + 1
        h.append(node)
    heapq.heapify(h)
    while len(h) != 1:
        right = heapq.heappop(h)
        left = heapq.heappop(h)
        newnode = TreeNode(freq = left.freq+right.freq,
                           left = left, right = right, rank = rank)
        rank = rank + 1
        heapq.heappush(h, newnode)
    # h[0] is the root of Huffman tree
    coding = {}
    dfs_for_coding(h[0], coding, "")
    return coding, h[0]

def dfs_for_coding(root, coding_dict, prefix):
    if root.symbol != None:
        coding_dict[root.symbol] = prefix
        return
    if root.left != None:
        dfs_for_coding(root.left, coding_dict, prefix+"0")
    if root.right != None:
        dfs_for_coding(root.right, coding_dict, prefix+"1")

def encode(seq, coding):
    """
    Return a list of 0-1 string that `seq` encoded by prefix-code
    implied by Huffman tree with `coding`
    """
    output = []
    for x in seq:
        output.append(coding[x])
    return output

def decode(seq, root, verbose = False):
    """
    Return a list of symbol that decoded by prefix-code
    implied by Huffman tree with `root`
    """
    output = []
    while len(seq) != 0:
        if verbose:
            print seq[:16],
        symbol, step = root.find_symbol(seq)
        if verbose:
            print step
        seq = seq[step:]
        output.append(symbol)
    return output
