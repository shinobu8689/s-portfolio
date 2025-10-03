"""
ADD COMMENTS TO THIS FILE 
"""
from typing import List, TypeVar

T = TypeVar('T')

def insertion_sort(the_list: List[T]):          # define function insertion_sort
    length = len(the_list)                      # get the length of the the_list
    for i in range(1, length):                  # loop for the length - 1 times for each array element
        key = the_list[i]                       # get the unsorted element as temp key.  key will be the one getting sorted
        j = i-1                                 # j = i - 1 for the range of sorted elements
        while j >= 0 and key < the_list[j] :    # loop only if j is >= 0 (to prevent getting out of the array range) and the next_value (key) is smaller than the_list[j]
                the_list[j + 1] = the_list[j]   # shifting the sorted elements where it lies between the_list[j - 1] <= key < the_list[j + 2]
                j -= 1                          # j -= 1 for next iteration to check the next unsorted element
        the_list[j + 1] = key                   # the next unsorted element as key

def main() -> None:
    arr = [6, -2, 7, 4, -10]
    insertion_sort(arr)
    for i in range(len(arr)):
        print (arr[i], end=" ")
    print()


main()