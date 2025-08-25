import numpy as np
from collections import Counter, defaultdict
import heapq
from bitarray import bitarray

class Node:
    def __init__(self, value=None, freq=0):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    heap = [Node(val, freq) for val, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(root):
    codes = {}
    def _traverse(node, code=""):
        if node.value is not None:
            codes[node.value] = bitarray(code)
            return
        _traverse(node.left, code + "0")
        _traverse(node.right, code + "1")
    _traverse(root)
    return codes

def compress_image_gray(image):
    flat = image.flatten()
    freq = Counter(flat)
    tree = build_huffman_tree(freq)
    codebook = generate_codes(tree)

    encoded = bitarray()
    for val in flat:
        encoded += codebook[val]

    return encoded, codebook, image.shape

def decompress_image_gray(encoded, codebook, shape):
    reverse_codebook = {v.to01(): k for k, v in codebook.items()}
    decoded = []
    temp = ""
    for bit in encoded.to01():
        temp += bit
        if temp in reverse_codebook:
            decoded.append(reverse_codebook[temp])
            temp = ""

    return np.array(decoded, dtype=np.uint8).reshape(shape)
