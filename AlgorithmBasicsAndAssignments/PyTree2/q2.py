import sys

# 32868901 Yin Lam Lo

class Node:
    def __init__(self, t):
        self.t = t
        self.valid_element = 0
        self.elements = [None] * (2 * t - 1)  # element: ord(element)
        self.valid_child = 0
        self.child = [None] * (2 * t)
        self.is_leaf = True

    def delete_e(self, pos):  # for leafs delete position's element and shift
        deleted_e = self.elements[pos]
        for i in range(self.valid_element - pos - 1):
            self.elements[i + pos] = self.elements[i + pos + 1]
        self.valid_element -= 1
        self.elements[self.valid_element] = None
        return deleted_e

    def delete_c(self, pos):  # for leafs delete position's child and shift
        deleted_c = self.child[pos]
        for i in range(self.valid_child - pos - 1):
            self.child[i + pos] = self.child[i + pos + 1]
        self.valid_child -= 1
        self.child[self.valid_child] = None
        return deleted_c

    def __str__(self):  # only for t = 3 for testing
        return f"{self.elements[0]} {self.elements[1]} {self.elements[2]} {self.elements[3]} {self.elements[4]} | {self.valid_element} Child:{self.valid_child} "


class BTree:
    def __init__(self, t):
        self.root = None
        self.t = t

    def _insert_in_leaf(self, node, element):
        i = node.valid_element - 1
        while i >= 0 and compare_string_lexical(element, node.elements[i]):  # shift
            node.elements[i + 1] = node.elements[i]
            i -= 1
        node.elements[i + 1] = element
        node.valid_element += 1

    def insert(self, current_node, element, parent_node=None):
        if self.root is None:  # if no root, new node as root
            self.root = Node(self.t)
            self.root.elements[0] = element
            self.root.valid_element += 1
        else:
            if current_node.valid_element == 2 * self.t - 1:  # if full, split the (sub)tree
                current_node = self._split_child(current_node, parent_node)
            if not current_node.is_leaf:
                i = 0
                while i < current_node.valid_element and current_node.elements[i] is not None:
                    if compare_string_lexical(element, current_node.elements[i]):  # insert to left child
                        self.insert(current_node.child[i], element, current_node)
                        break
                    elif i == current_node.valid_element - 1:  # insert to right child
                        self.insert(current_node.child[i + 1], element, current_node)
                        break
                    i += 1
            else:  # insert to this
                if self.binary_search(element, current_node) == -1:
                    self._insert_in_leaf(current_node, element) # insert of not already exist

    def _split_child(self, node, parent=None):
        median = int((2 * self.t - 1) / 2)
        if parent is None:  # rise median to parent
            combine_flag = False
            parent = Node(self.t)
            self.root = parent
        else:
            combine_flag = True

        # shift to make space for raised child
        i = parent.valid_element - 1
        while i >= 0 and compare_string_lexical(node.elements[median], parent.elements[i]):
            parent.elements[i + 1] = parent.elements[i]
            parent.child[i + 2] = parent.child[i + 1]
            parent.child[i + 1] = parent.child[i]
            i -= 1
        i += 1
        parent.elements[i] = node.elements[median]
        parent.valid_element += 1
        parent.is_leaf = False

        # teap store the splitted node
        split_L = self.create_sub_node(node.elements[:median], node.child[:median + 1], node.is_leaf)
        split_R = self.create_sub_node(node.elements[median + 1:], node.child[median + 1:], node.is_leaf)

        if combine_flag:  # merge to existing parent
            parent.child[i] = split_L
            parent.child[i + 1] = split_R
            parent.valid_child += 1
        else:  # add to new node
            parent.child[parent.valid_child] = split_L
            parent.valid_child += 1
            parent.child[parent.valid_child] = split_R
            parent.valid_child += 1
        return parent

    def binary_search(self, element, node):
        low, high = 0, node.valid_element - 1
        while low <= high:
            mid = (low + high) // 2
            if node.elements[mid] == element:
                return mid
            elif compare_string_lexical(node.elements[mid], element):
                low = mid + 1
            else:
                high = mid - 1
        return -1   # not found

    def create_sub_node(self, elements, child, leaf):  # take its splitted element and child to from a new node
        splitted = Node(self.t)
        splitted.elements = elements + [None] * (2 * self.t - 1 - len(elements))
        splitted.valid_element = len(elements)
        if not leaf:
            splitted.child = child + [None] * (2 * self.t - len(child))
            splitted.valid_child = 2 * self.t - splitted.child.count(None)
            splitted.is_leaf = False
        return splitted

    def delete(self, current_node: Node, target, parent_node=None, current_in_parent_i=None):
        i = 0
        if parent_node is not None and current_node.valid_element == self.t - 1 and not current_node.is_leaf:  # left most
            current = self.merge_from_above(current_node, parent_node, current_in_parent_i)
            self.root = current  # set combined node as new node

        while i <= current_node.valid_element - 1:
            if compare_string_lexical(target, current_node.elements[i]):  # traverse to left
                self.delete(current_node.child[i], target, current_node, i)
                break
            elif i == current_node.valid_element and compare_string_lexical(current_node.elements[i], target):  # traverse to right
                self.delete(current_node.child[i + 1], target, current_node, i)
                break
            elif target == current_node.elements[i]:  # found
                if current_node.is_leaf:  # delete_in_leaf
                    current_node.delete_e(i)
                    if current_node.valid_element < self.t - 1:
                        self.rotate_with_sibling(current_node, parent_node, current_in_parent_i)
                else:  # not leaf
                    self.case2(current_node, i, parent_node)
                break
            i += 1
        # end up here if cannot find to delete (do nothing)

    def get_replacement(self, parent: Node, node_pos: int, right_most):
        '''
        recursive find its replacement for element in the middle, return the found element and remove from its original pos
        '''
        node = parent.child[node_pos]
        if not node.is_leaf:
            return self.get_replacement(parent, 0 if right_most else node.valid_child, right_most)
        else:
            replacement = node.delete_e(0 if right_most else node.valid_element - 1)
            return replacement, node, parent, node_pos

    def merge_child(self, current: Node, l: int, r: int):
        '''
        merge all in right to left
        '''
        left = current.child[l]
        right = current.child[r]
        for i in range(right.valid_element):    # merge elements
            left.elements[left.valid_element] = right.elements[i]
            left.valid_element += 1
        if left.valid_child > 0 or right.valid_child > 0:   # child in the middle combines into one child
            self.merge_child(left.child[left.valid_child - 1], right.child[0])
        for i in range(right.valid_child - 1):  # combine remain child
            left.child[left.valid_child] = right.child[i + 1]
            left.valid_child += 1

        i = r
        while i < current.valid_child - 1:
            current.child[i] = current.child[i + 1]
            i += 1
        current.child[current.valid_child - 1] = None
        current.valid_child -= 1

    def case2(self, current_node: Node, pos, parent_node):
        if pos == current_node.valid_element - 1 and pos == 0: # its the root w/ only element
            pos = current_node.child[0].valid_element
            self.merge_from_above(current_node.child[0], current_node, 0)
            self.root = current_node.child[0]
            current_node = current_node.child[0]

        if pos == current_node.valid_element - 1:  # right most element
            # take the largest from left subtree
            current_node.elements[pos], taken_from_node, its_parent, parent_i = self.get_replacement(current_node, pos, False)
            if taken_from_node.valid_element < self.t - 1: self.rotate_with_sibling(taken_from_node, its_parent, parent_i)
        elif pos == 0:  # left most element
            # take the smallest from right subtree
            current_node.elements[pos], taken_from_node, its_parent, parent_i = self.get_replacement(current_node, pos + 1, True)
            if taken_from_node.valid_element < self.t - 1: self.rotate_with_sibling(taken_from_node, its_parent, parent_i)
        else:  # its somewhere in the middle
            # if merge exceeds limit
            if (current_node.child[pos].valid_element + current_node.child[pos + 1].valid_element) >= self.t * 2:
                if current_node.child[pos].valid_element > current_node.child[pos + 1].valid_element:
                    self.get_replacement(current_node, pos, False)
                else:
                    self.get_replacement(current_node, pos + 1, True)
            else:
                self.merge_child(current_node, pos, pos + 1)
                current_node.delete_e(pos)

    def merge_from_above(self, current: Node, parent: Node, parent_i: int):
        # current is not the leftest/rightest child of parent, check left/right sibling min element?
        if parent_i != 0 and parent.child[parent_i].valid_element == self.t - 1:
            sibling = parent.child[parent_i - 1]
        elif parent_i != parent.valid_child and parent.child[parent_i + 1].valid_element == self.t - 1:
            sibling = parent.child[parent_i + 1]

        # combine all ele/child into current
        for element in range(parent.valid_element):
            current.elements[current.valid_element] = parent.elements[element]
            current.valid_element += 1
        for element in range(sibling.valid_element):
            current.elements[current.valid_element] = sibling.elements[element]
            current.valid_element += 1
        for child in range(sibling.valid_child):
            current.child[current.valid_child] = sibling.child[child]
            current.valid_child += 1
        return current

    def rotate_with_sibling(self, current: Node, parent: Node, parent_i: int):  # rotate if t - 1 element
        # current is not the leftest/rightest child of parent, check left/right sibling
        if parent_i != 0 and parent.child[parent_i - 1].valid_element > self.t - 1: # have ele to swap
            sibling = parent.child[parent_i - 1]
        elif parent_i != parent.valid_child and parent.child[parent_i + 1].valid_element > self.t - 1:  # have ele to swap
            sibling = parent.child[parent_i + 1]
        else:  # no suitable sibling, merge to nearby
            if parent_i != parent.valid_child and parent.child[parent_i + 1].valid_element >= self.t - 3: dest = parent_i + 1
            elif parent_i != 0 and parent.child[parent_i - 1].valid_element >= self.t - 3: dest = parent_i - 1
            self.insert(parent.child[dest], parent.elements[parent_i])
            self.insert(parent.child[dest], parent.child[parent_i].elements[0])
            parent.delete_e(parent_i)
            parent.delete_c(parent_i)
            return
        self.insert(current, parent.elements[parent_i])  # current <- parent
        parent.elements[parent_i] = sibling.elements[0]  # parent <- sibling
        sibling.delete_e(0)

    def print(self, node: Node):
        '''
        print from leftest child to right child, if None (no child) print element
        '''
        i = 0
        while i <= node.valid_element:
            if node.child[i] is not None: self.print(node.child[i])
            if node.elements[i] is not None: f.write(f'{node.elements[i]}\n') # print(node.elements[i])
            i += 1
        if node.child[i] is not None: self.print(node.child[i])


def compare_string_lexical(str1, str2):  # 1 smaller/shorter than 2
    '''
    for each char, compare, return immediately when unmatched   O(n)
    '''
    for i in range(min(len(str1), len(str2))):
        if str1[i] < str2[i]:
            return True
        elif str1[i] > str2[i]:
            return False
    return len(str1) < len(str2)  # strings are identical or 2 is longer


def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


if __name__ == "__main__":
    _, t, dict_file, comm_file = sys.argv
    t = int(t)
    tree = BTree(t)

    lst = read_file(dict_file)
    for each in range(len(lst)):
        lst[each] = lst[each].strip()

    for i in lst:
        tree.insert(tree.root, i)

    command = read_file(comm_file)
    for each in range(len(command)):
        command[each] = command[each].strip().split(" ")
        if command[each][0] == "insert":
            tree.insert(tree.root, command[each][1])
        elif command[each][0] == "delete":
            tree.delete(tree.root, command[each][1])

    f = open("output_q2.txt", "x")
    # tree.print(tree.root)
    f.close()




