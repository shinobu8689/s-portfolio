""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
"""
from __future__ import annotations

__author__ = 'Brendon Taylor. Modified by Graeme Gange, Alexey Ignatiev, Jackson Goerner, and Alexis Baraka Mcharo'
__docformat__ = 'reStructuredText'
__modified__ = '07/10/2022'
__since__ = '14/05/2020'


from primes import LargestPrimeIterator
from referential_array import ArrayR
from typing import TypeVar, Generic

T = TypeVar('T')


class LinearProbeTable(Generic[T]):
    """
        Linear Probe Table.

        attributes:
            count: number of elements in the hash table
            table: used to represent our internal array
            tablesize: current size of the hash table
    """

    def __init__(self, expected_size: int, tablesize_override: int = -1) -> None:
        """
            Initialiser.
        """

        self.count = 0
        if tablesize_override == -1:
            l = LargestPrimeIterator(expected_size, 5)
            next(l)
            prime = next(l)
            self.tablesize = prime
        else:
            self.tablesize = tablesize_override
        self.table = ArrayR(self.tablesize)
        self.conflict = 0
        self.probe_total = 0
        self.probe_max = 0
        self.rehash = 0

    def hash(self, key: str) -> int:
        """
            Hash a key for insertion into the hashtable.
        """
        # value = 0
        # for char in key:
        #     value = (value * 31 + ord(char)) % self.tablesize
        # return value

        value = 0
        a = 31
        hash_base =31
        for char in key:
            value = (ord(char) + a * value) % self.tablesize
            a = a * hash_base % (self.tablesize - 1)
        return value

    def statistics(self) -> tuple:
        return self.conflict, self.probe_total, self.probe_max, self.rehash

    def __len__(self) -> int:
        """
            Returns number of elements in the hash table
            :complexity: O(1)
        """
        return self.count

    def _linear_probe(self, key: str, is_insert: bool) -> int:
        """
            Find the correct position for this key in the hash table using linear probing
            :complexity best: O(K) first position is empty
                            where K is the size of the key
            :complexity worst: O(K + N) when we've searched the entire table
                            where N is the tablesize
            :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)
        max_probe = 0
        has_collided = False
        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot
                if is_insert:
                    return position
                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position
            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)
                if not has_collided:
                    has_collided = True
                    self.conflict += 1
                self.probe_total += 1
                max_probe += 1
                self.probe_max = max(self.probe_max, max_probe)


        raise KeyError(key)

    def keys(self) -> list[str]:
        """
            Returns all keys in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][0])
        return res

    def values(self) -> list[T]:
        """
            Returns all values in the hash table.
        """
        res = []
        for x in range(len(self.table)):
            if self.table[x] is not None:
                res.append(self.table[x][1])
        return res

    def __contains__(self, key: str) -> bool:
        """
            Checks to see if the given key is in the Hash Table
            :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
            Get the item at a certain key
            :see: #self._linear_probe(key: str, is_insert: bool)
            :raises KeyError: when the item doesn't exist
        """
        position = self._linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
            Set an (key, data) pair in our hash table
            :see: #self._linear_probe(key: str, is_insert: bool)
            :see: #self.__contains__(key: str)
        """
        try:
            position = self._linear_probe(key, True)
        except KeyError:
            self._rehash()
            self.__setitem__(key, data)
        else:
            if self.count > self.tablesize / 2:
                self._rehash()
            if self.table[position] is None:
                self.count += 1
            self.table[position] = (key, data)

    def __delitem__(self, key: str) -> None:
        """
        Deletes an item from our hash table by rehashing the
        remaining items in the current primary cluster
        :raises KeyError: when the key doesn't exist
        :complexity best: O(K) finds the position straight away and doesn't have to rehash
                          where K is the size of the key
        :complexity worst: O(K + N) when it has to rehash all items in the hash table
                          where N is the table size
        """
        position = self._linear_probe(key, False)
        self.table[position] = None
        self.count -= 1

        position = (position + 1) % len(self.table)
        while self.table[position] is not None:
            item = self.table[position]
            self.table[position] = None
            self.count -= 1
            self[str(item[0])] = item[1]
            position = (position + 1) % len(self.table)


    def is_empty(self):
        """
            Returns whether the hash table is empty
            :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
            Returns whether the hash table is full
            :complexity: O(1)
        """
        return self.count == len(self.table)

    def insert(self, key: str, data: T) -> None:
        """
            Utility method to call our setitem method
            :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def _rehash(self) -> None:
        """
            Need to resize table and reinsert all values
        """
        l = LargestPrimeIterator(self.tablesize, 5)
        next(l)
        next_prime = next(l)
        new_hash = LinearProbeTable(self.tablesize, next_prime)
        for i in range(len(self.table)):
            if self.table[i] is not None:
                new_hash[str(self.table[i][0])] = self.table[i][1]

        self.count = new_hash.count
        self.table = new_hash.table
        self.tablesize = new_hash.tablesize
        self.rehash += 1

    def __str__(self) -> str:
        """
            Returns all they key/value pairs in our hash table (no particular
            order).
            :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

if __name__ == '__main__':
    aus = open('aust_cities.txt','r')
    aus_cities = aus.read()
    aus_cities = aus_cities.split('\n')
    aus.close()

    ind = open('indian_cities.txt','r')
    ind_cities = ind.read()
    ind_cities = ind_cities.split('\n')
    ind.close()

    us = open('us_cities.txt','r')
    us_cities = us.read()
    us_cities = us_cities.split('\n')
    us.close()

    #for the indian cities
    l_ind = LinearProbeTable(len(ind_cities),len(ind_cities))
    for i in range(len(ind_cities)):
        l_ind.__setitem__(ind_cities[i], i)
    print("Indian cities statistics: ", l_ind.statistics())
    print("Number of Indian cities:", len(ind_cities))
    print("\n")

    #for the aus cities
    l_aus = LinearProbeTable(len(aus_cities),len(aus_cities))
    for i in range(len(aus_cities)):
        l_aus.__setitem__(aus_cities[i],i)
    print("Australian cities statistics: ",l_aus.statistics())
    print("Number of Australian cities: ", len(aus_cities))
    print("\n")

    #for the us cities
    l_us = LinearProbeTable(len(us_cities),len(us_cities))
    for i in range(len(us_cities)):
        l_us.__setitem__(us_cities[i], i)
    print("US cities statistics: ", l_us.statistics())
    print("Number of US cities: ", len(us_cities))

