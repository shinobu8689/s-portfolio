import copy
import sys
from bitarray import bitarray


# 32868901 Yin Lam Lo

def bwt_transform(string: str) -> str:
    """
    O(n log n), where n = the length of str
    :param string: original str
    :return: str in bwt
    """
    matrix = []
    bwt_str = ""
    for i in range(len(string)): matrix.append(string[-i:] + string[:-i])  # string rotation O(n)
    matrix.sort()  # O(n log n)
    for i in matrix: bwt_str += i[-1]  # take last row   O(n)
    return bwt_str


def elias_encode(number: int) -> bitarray:
    '''
    O(log n)
    :param number:
    :return:    number in elias code
    '''
    elias_l = []  # store each iter

    binary = bitarray(bin(number)[2:])  # L1    O(log n), slice for removing "0b"
    elias_l.append(binary)

    while len(binary) != 1:             # L2 onwards      O(log n)
        binary = bitarray(bin(len(binary) - 1)[2:])     # O(log n)
        binary[0] = 0 if binary[0] == 1 else 1          # flip
        elias_l.append(binary)

    elias_code = bitarray()
    for ln in reversed(elias_l):  # O(log n)
        elias_code.extend(ln)
    return elias_code


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


def grow(node0: Node, node1: Node) -> Node:
    '''
    # O(1)
    :param node0:
    :param node1:
    :return:
    '''
    return Node(node0.string + node1.string, node0.appearance + node1.appearance, [node0, node1])


def build_tree(node_list: list[Node]) -> Node:
    '''
    O(n log n)
    build tree with the given list
    :param node_list:
    :return:
    '''
    root = Node()
    while len(node_list) > 1:   # O(n log n)
        node_list = sorted(node_list, key=lambda x: x.appearance)
        root = grow(node_list[0], node_list[1])
        node_list = node_list[2:]
        node_list.append(root)
    return root


def huffman_encode(string: str) -> list[(str, bitarray)]:  # create huffman code list
    '''
    # O(n log n), n = string length
    :param string:
    :return:
    '''
    # create char appearance list
    char_appearance = [0] * 256
    for _char in string: char_appearance[ord(_char)] += 1   # O(n)

    node_list = []  # given ascii range 36, 126  turn all item into node   O(91)
    for _char in range(36, 127):
        if char_appearance[_char] > 0: node_list.append(Node(chr(_char), char_appearance[_char]))

    tree = build_tree(node_list)        # O(n log n)
    code_list = search_code(tree)       # O(n)

    return code_list


def search_code(tree: Node, codeword: bitarray = bitarray()) -> list[(str, bitarray)]:
    '''
    # O(n), n = number of nodes
    :param tree:
    :param codeword:
    :return:
    '''
    code_list = []
    if tree.children == [None, None]:
        code_list.append((tree.string, codeword))
        return code_list
    if tree.children[0] is not None:
        codeword_this_level = copy.deepcopy(codeword)   # O(n)
        codeword_this_level.append(0)
        code_list += search_code(tree.children[0], codeword_this_level) # O(n)
    if tree.children[1] is not None:
        codeword_this_level = copy.deepcopy(codeword)   # O(n)
        codeword_this_level.append(1)
        code_list += search_code(tree.children[1], codeword_this_level) # O(n)
    return code_list


def to_ascii(_char: str) -> bitarray:
    '''
    O(1), give 7 bit ascii
    :param _char:
    :return:
    '''
    return bitarray((7 - len(bin(ord(_char))[2:])) * "0" + bin(ord(_char))[2:])


def runlength_encode(string: str) -> list[(str, int)]:
    '''
    O(n), n = string length
    :param string:
    :return:
    '''
    list_of_runlength = []
    for i in range(len(string)):
        if len(list_of_runlength) == 0:
            list_of_runlength.append((string[i], 1))
        else:
            if string[i] is not list_of_runlength[-1][0]:
                list_of_runlength.append((string[i], 1))
            else:
                list_of_runlength[-1] = (string[i], list_of_runlength[-1][1] + 1)
    return list_of_runlength


def char_from_huffman_list(huffman: list[(str, str)], char: str) -> str:  # get corresponding char for huffman code
    '''
    O(91), where O(n),n = 91
    given that the ascii range 36, 126, and worst case all char in str is all unique
    :param huffman:
    :param char:
    :return:
    '''

    for i in huffman:
        if i[0] == char:
            return i[1]


def encode(input_str: str) -> bitarray:
    '''
    # O(n log n), n = string length, build up the encoded code for whole encoding
    :param input_str:
    :return:
    '''

    bwt = bwt_transform(input_str)                  # O(n log n)
    bwt_elias = elias_encode(len(bwt))              # O(b^2), b = int.bit_length()
    huffman_code = huffman_encode(bwt)              # O(n log n)
    runlength_code = runlength_encode(bwt)          # O(n)
    n_char_elias = elias_encode(len(huffman_code))  # O(b^2), b = int.bit_length()

    encoded = bitarray()
    encoded += bwt_elias + n_char_elias
    for i in huffman_code:      # O(n)
        encoded += to_ascii(i[0]) + elias_encode(len(i[1])) + i[1]  # ascii
    for i in runlength_code:    # O(n)
        encoded += char_from_huffman_list(huffman_code, i[0]) + elias_encode(i[1])  # string
    return encoded


def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


if __name__ == "__main__":
    _, str_file = sys.argv
    input_s = read_file(str_file)[0]
    code = encode(input_s)
    code = str(code)[10:-2]  # turn into str for print

    f = open("q2_encoder_output.bin", "x")
    f.write(code)
    f.close()
