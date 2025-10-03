"""
ADD COMMENTS TO THIS FILE 
"""


def print_combination(arr, n, r):

    data = [0] * r
 
    combination_aux(arr, n, r, 0, data, 0)
 
def combination_aux(arr, n, r, index, data, i): #define the function combination_aux

    if (index == r):                        # if this function get recursion called enough times that index == r
        for j in range(r):                  # for all element in data
            print(data[j], end = " ")       # print all element in data
        print()                             # print a new line, which each time the array prints will be one single one
        return                              # return function & wont recall itself again
 
    if (i >= n):                            # if the function get recursion called enough times that i >= n
        return                              # return function & wont recall itself again
 
    data[index] = arr[i]                    # putting item from arr to data through each recursion
    combination_aux(arr, n, r, index + 1,   # call itself again for next element in data
                    data, i + 1)            # with the next value of arr
 
    combination_aux(arr, n, r, index,       # call itself again to change that data element
                    data, i + 1)            # with the next value of arr, slowly work its way to getting the last 3 element to data
 
def main():
    arr = [1, 2, 3, 4, 5]
    r = 3
    n = len(arr)
    print_combination(arr, n, r)

main()