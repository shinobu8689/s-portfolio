import sys

from bitarray import bitarray
from bitarray.util import ba2int


# 32868901 Yin Lam Lo

def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


class Node:
    def __init__(self, string="", appearance=0, children=[None, None]):
        '''
        # O(1)
        :param string:
        :param appearance:
        :param children:
        '''
        self.string = string
        self.appearance = appearance
        self.children = children

    def __str__(self):
        return self.string + ":" + str(self.appearance)


def huffman_decode(tree: Node, codeword: str) -> (str, str):
    '''
    O(k), k = the longest (deepest in tree) huffman code
    decode 1 char of bits
    :param tree:
    :param codeword:
    :return:
    '''
    current = tree
    shift = 0
    for bit in codeword:    # O(k), k = the longest huffman code
        if current.children[int(bit)] is not None:  # follow the tree
            current = current.children[int(bit)]
            shift += 1
        else:
            return current.string, codeword[shift:]


def tree_from_huffman_list(huffman: list[(str, bitarray)]) -> Node:
    '''
    # O(n), n = number of unique char, where all char in str in unique
    :param huffman:
    :return:
    '''
    root = Node()
    for char in huffman:    # O(n), n = number of unique char, where all char in str in unique
        current = root
        for bit in char[1]: # new child for new
            if current.children[int(bit)] is None:  current.children[int(bit)] = Node(char[0], children=[None, None])
            current = current.children[int(bit)]
    return root


def elias_decode(codeword: bitarray) -> (int, bitarray):
    '''
    O(k), k = number of 1 of each L
    :param codeword:
    :return:
    '''
    n = 0                       # current value of L
    pos = 0
    length = 0                  # length of this elias code section
    component = bitarray('1')   # startup decode

    while component[0] != 0:    # O(k)
        component = codeword[pos:pos + n + 1]
        component[0] = 1 if component[0] == 0 else 0  # filp
        length += n + 1     # shift bits
        pos += n + 1
        if component[0] == 1: n = ba2int(component)

    component[0] = 1  # flip for last
    return ba2int(component), codeword[length:]


def decode(remain: bitarray) -> str:
    bwt_length, remain = elias_decode(remain)    # O(k)
    char_len, remain = elias_decode(remain)      # O(k)

    huffman_code = []
    for i in range(char_len):                    # get char to huffman
        current_char = chr(ba2int(remain[:7]))
        remain = remain[7:]                      # remove read ascii bits
        char_len, remain = elias_decode(remain)
        huffman_code.append((current_char, remain[:char_len]))
        remain = remain[char_len:]               # remove read huffman bits

    tree = tree_from_huffman_list(huffman_code)

    original = []
    while len(remain) > 0:  # O(n)  build string with runlength
        char, remain = huffman_decode(tree, remain)
        appearance, remain = elias_decode(remain)
        original.append(char * appearance)
    return bwt_recover(''.join(original))       # O(n log n)


def bwt_recover(last):
    '''
    O(n log n)
    :param last:
    :return:
    '''
    first = []
    original = "$"
    rank_lst = [None] * 256

    for i in last: first.append(i)              # O(n)  get first col
    first.sort()                                # O(n log n)
    unique_char = sorted(list(set(first)))      # O(n log n + 2n)

    unique_char_position = 0  # create rank_lst
    str_position = 0
    while unique_char_position < len(unique_char):  # O(n)
        if unique_char[unique_char_position] == first[str_position]:
            rank_lst[ord(first[str_position])] = str_position
            unique_char_position += 1
        str_position += 1

    pos = 0
    while last[pos] != "$":  # O(n)     recover the original str
        i = pos
        rank = rank_lst[ord(last[i])]
        n_occurrences = last[:i].count(last[i])
        original = last[i] + original
        pos = rank + n_occurrences

    return original


if __name__ == "__main__":
    _, code_file = sys.argv
    code = read_file(code_file)[0]
    decoded_str = decode(bitarray(code))
    f = open("q2_decoder_output.txt", "x")
    f.write(decoded_str)
    f.close()
