""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev, with edits by Jackson Goerner'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic, List
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """
        Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)

            :returns: int height_of_tree
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert via recursion
        """
        if not current:
            self.length += 1
            return AVLTreeNode(key, item)
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)

        current.length_node += 1
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1

        return self.rebalance(current)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """

        if not current:
            self.length -= 1
            return current
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:
            if current.left == None:
                temp = current.right
                current = None
                return temp
            elif current.right == None:
                temp = current.left
                current = None
                return temp

            temp = self.get_minimal(current.right)
            current.key = temp.key
            current.right = self.delete_aux(current.right, temp.key)
            current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1

            return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        RotatedAVL = current.right
        Temp = RotatedAVL.left
        RotatedAVL.left = current
        current.right = Temp
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        RotatedAVL.height = max(self.get_height(RotatedAVL.left), self.get_height(RotatedAVL.right)) + 1

        current.length_node = 1
        if current.left:
            current.length_node += current.left.length_node
        if Temp:
            current.length_node += Temp.length_node

        RotatedAVL.length_node = 1 + current.length_node
        if RotatedAVL.right:
            RotatedAVL.length_node = RotatedAVL.right.length_node

        return RotatedAVL

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        RotatedAVL = current.left
        Temp = RotatedAVL.right
        RotatedAVL.right = current
        current.left = Temp
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        RotatedAVL.height = 1 + max(self.get_height(RotatedAVL.left), self.get_height(RotatedAVL.right))

        current.length_node = 1
        if current.left:
            current.length_node += current.left.length_node
        if Temp:
            current.length_node += Temp.length_node

        RotatedAVL.length_node = 1 + current.length_node
        if RotatedAVL.left:
            RotatedAVL.length_node += RotatedAVL.left.length_node

        return RotatedAVL

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def range_between_aux(self, current: AVLTreeNode, i: int, j, range_list=None):
        """

        :param current: the current avl tree node
        :param i: the lower bound
        :param j: the upper bound
        :param range_list: the range list that will be filled with keys
        :return: returns the range list
        :complexity: O(j - i + log(n))
        """
        if range_list is None:
            range_list = []

        AVLTree_Length = 0
        if current.left:
            AVLTree_Length = current.left.length_node

        if current.left and AVLTree_Length > i:
            self.range_between_aux(current.left, i, j, range_list)
        if i <= AVLTree_Length <= j:
            range_list.append(current.key)
        if current.right and AVLTree_Length < j:
            self.range_between_aux(current.right, i-AVLTree_Length-1, j-AVLTree_Length-1, range_list)

        return range_list

    def range_between(self, i: int, j: int) -> List:
        """
        Returns a sorted list of all elements in the tree between the ith and jth indices, inclusive.
        :complexity: O(j - i + log(n))
        """
        return self.range_between_aux(self.root, i, j, [])

if __name__ == "__main__":
    import random
    random.seed(16)
    numbers = list(range(0, 100))
    tree = AVLTree()
    length = random.randint(10, 100)
    for num in numbers[:length]:
        tree[num] = num
    # self.assertEqual(tree.range_between(1, 5), [2, 3, 4, 5, 6], "Range between failed")
