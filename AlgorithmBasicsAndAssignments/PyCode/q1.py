import sys


# 32868901 Yin Lam Lo


def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line

class Node:
    def __init__(self, start=None, end=None, children=None, is_leaf=True, pos_in_str=None):
        '''O(1)'''
        self.start = start      # trick 1 – space-efficient representation of edge-labels/substrings
        self.end = end          # sub string = str[start:end]
        self.is_leaf = is_leaf  # have child, mark directly to avoid checking children list
        self.children = children or [None] * 256  # init all possible char
        self.pos_in_str = pos_in_str

    def __str__(self):
        return f'[{self.start}:{self.end.end}]"{input_str[self.start:self.end.end+1]}" ({self.pos_in_str})'


class Leaf:  # global end for all leafs used for update at each cycle
    def __init__(self, end):
        self.end = end

    def __str__(self):
        return self.end


class SuffixTree:
    def __init__(self, string):
        self.leaf = Leaf(-1)
        self.root = Node(-1, Leaf(-1), None, False)
        self.traverse_order = self.create_traverse_lst(string)  # lst of order for position to follow
        self.str_rank = [None] * len(string)    # str_rank[position] = rank, list of ranks

        self.ukkonen(string)

        self.rank = 1
        self.traverse_node(self.root)   # fill in rank array
        print(self.str_rank)

    def traverse_node(self, node):
        '''
        # go through the tree following the traverse_order
        O(n), n = number of nodes
        :param node: root node of tree/subtree
        :return:
        '''
        for i in self.traverse_order:
            if node.children[i] is not None:
                if node.children[i].is_leaf:
                    print(f"--- {node.children[i]} <= rank{self.rank}")
                    self.str_rank[node.children[i].pos_in_str] = self.rank
                    self.rank += 1
                self.traverse_node(node.children[i])

    def create_traverse_lst(self, string):
        '''
        # take all unique letters from str and convert to position using ord, O(n), n = given string
        :param string: given string
        :return:
        '''
        str_lst = set()
        for i in string: str_lst.add(i)
        str_lst = list(str_lst)
        str_lst.sort()
        for i in range(len(str_lst)): str_lst[i] = ord(str_lst[i])
        return str_lst

    def ukkonen(self, string_input):
        frame_start = 0
        for frame_end in range(len(string_input)):  # each phase
            phase_str = string_input[frame_start:frame_end+1]
            self.leaf.end = frame_end  # rule1 - extend, + trick4 rapid extend (extend first, split later)
            current_processing_pos = 0
            next_node = self.root   # node pending to be as current in next cycle
            skipped_length = 0
            skipped_time = 0

            while frame_start < frame_end + 1:  # each substring in that phase
                current_node = next_node
                if current_node.children[ord(phase_str[current_processing_pos])] is not None:  # move to child
                    parent_node = current_node
                    current_node = current_node.children[ord(phase_str[current_processing_pos])]
                    frame_length = frame_end - frame_start
                    # go to rule3 if char at current stage str end == char of current node + frame_len
                    if string_input[current_node.start + frame_length] == string_input[frame_end]:
                        break  # rule3 - node exist, nothing + trick3 – premature extension stopping criterion
                        # do not change frame_start, expanding the frame
                        # all leaves extend through global, no need to go through previous char for redundant comparison
                        # frame_start is where the splitting starts when new char appeared later at the string
                    else:
                        node_length = current_node.end.end - current_node.start + 1
                        if node_length <= frame_length:      # trick2 – skip/count
                            current_processing_pos += 1      # account for skipped amount when splitting
                            skipped_time += 1
                            skipped_length += node_length    # total skipped amount
                            next_node = current_node         # jump to node and use it base
                            continue

                        # rule2 - split current node into: first_half, second_half (of the previous existing node) + new_branch
                        first_half = Node(current_node.start, Leaf(current_node.start + frame_length - skipped_length - 1) , None, False, current_node.pos_in_str)    # dispatch from leaf end
                        second_half = Node(current_node.start + frame_length - skipped_length, current_node.end, current_node.children, current_node.is_leaf, current_node.pos_in_str)
                        new_branch = Node(frame_end, self.leaf, None, True, frame_start)

                        # link to first_half.children
                        first_half.children[ord(string_input[current_node.start + frame_length - skipped_length])] = second_half
                        first_half.children[ord(string_input[frame_end])] = new_branch

                        # link first_half to parent
                        parent_node.children[ord(string_input[current_node.start])] = first_half
                else:
                    current_node.children[ord(phase_str[current_processing_pos])] = Node(frame_start + skipped_length, self.leaf, None, True, frame_start)
                    current_node.is_leaf = False    # rule2 - branch

                # end of any branch/split
                next_node = self.root
                frame_start += 1    # increment frame_start to avoid redundant comparison
                current_processing_pos += 1
                if skipped_time > 0:   # reset skipped counters
                    skipped_length = 0
                    current_processing_pos -= skipped_time
                    skipped_time = 0


if __name__ == "__main__":
    _, filename1, filename2 = sys.argv
    input_str = read_file(filename1)[0]
    rank_from_position = read_file(filename2)
    tree = SuffixTree(input_str)  # create suffix tree

    f = open("output_q1.txt", "x")
    for i in range(len(rank_from_position)):    # take the row value and check it through str_rank
        rank_from_position[i] = tree.str_rank[int(rank_from_position[i].strip()) - 1]
        f.write(str(rank_from_position[i]) + "\n")
    print(rank_from_position)

    f.close()
