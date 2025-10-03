""""""

from __future__ import annotations

__author__ = 'Alexis Baraka Mcharo'
__docformat__ = 'reStructuredText'

import random_gen


class LargestPrimeIterator():
    def __init__(self, upper_bound: int, factor: int) -> None:
        '''
            Initialises LargestPrimeIterator
            Parameters: upper_bound (int), factor (int)
            Return:     None
            Complexity: O(1)
        '''
        self.upper_bound = upper_bound
        self.factor = factor

    def __iter__(self) -> LargestPrimeIterator:
        '''
            return the first iteration of LargestPrimeIterator
            Parameters: None
            Return:     self (LargestPrimeIterator)
            Complexity: O(1)
        '''
        return self

    def __next__(self) -> int:
        '''
            the action within iteration
            Parameters: None
            Return:     prime_number (int)
            Complexity: O(upper_bound^2)
        '''
        if self.upper_bound > 1:
            number_list = []
            for i in range(2, self.upper_bound):
                number_list.append(i)
            for i in range(2, self.upper_bound):
                for n in number_list:
                    if not n == i:
                        if n % i == 0:
                            number_list.remove(n)
            prime_number = number_list[-1]
            self.upper_bound = prime_number * self.factor
            return prime_number


"""if __name__ == '__main__':
    l = LargestPrimeIterator(6, 2)
    for i in range(6):
        prime = next(l)
        print(prime)"""
