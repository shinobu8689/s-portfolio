import heapq  # O(log n) for push and pop

# code by 32868901, Yin Lam LO for FIT2001 A1, 2023 S1

def optimalRoute(start, end, passengers, roads):
    '''
        Function description:   This functions takes the graph and modify it to suit our problem and return the path that take shortest time.
        Approach description:   In order to sort our problem, the graph needs to be modified. Variable roads is our
                                graph.  Let there be x nodes and y edges, we double the graph according to each lane.
                                Edge (x, y, 10, 2) will turn into (x1, y1, 10) and (x2, y2, 2).  Where the original
                                nodes and containing passenger will be connected with an edge with weight 0, which means
                                once they picked up passengers they could switch lane into T3 lane. And the time cost
                                for they to switch lane will be 0.  Since its 0, switching lanes will be consider by
                                dijkstra since it is a greedy algorithm.
                                However after the modification, the nodes numbering needs to be in order for the list
                                position to work.  For this case, every original node will have a *2 node and a *2+1 node
                                which if the node number is even then its in T3 lane, if its odd its in normal lane.
                                Here is how the mapping works: assume there is 0 to 4 nodes
                                original nodes:     0   1   2   3   4

                                original*2:         0   2   4   6   8       these will be the number for T3 lane
                                original*2+1:       1   3   5   7   9       these will be the number for normal lane

                                those modified number will not create duplicated and in order.  The modified graph will
                                be send to dijkstra to search for the fastest path.
                                to get the result of the path which needs to reverse back to the original numbering,
                                please look at shortest_path_retrieval(pred, target) which do the reversing.

        Input:  start:  indicate which node is the source of the original graph
                end:    indicate which node is the end of the original graph
                passenger:  list of which node has passenger in it, when going through these nodes, it can switch to T3 lane
                roads:  list that contains network of edges.

        Output: the fastest path from start to end

        Time complexity:        O(R) + O(P) + O(R log L) = O(R log L)
        Aux space complexity:   O(R) + O(2L) = O(L + R)
    '''
    new_graph = []                                              # Modify the graph, space complexity = O(2R+ P)
    for road in roads:                                          # O(R)
        new_graph.append((road[0]*2+1 , road[1]*2+1, road[2]))  # odd = normal
        new_graph.append((road[0]*2, road[1]*2, road[3]))       # even = T3 Lane
    for passenger in passengers:                                # O(P)
        new_graph.append((passenger*2+1, passenger*2, 0))
    return dijkstra(new_graph, start, end)                       #O(R log L)

def dijkstra(graph, start, end):
    '''
        Function description:   This function get the graph and return the shortest path.
        Approach description:   To operate, It works with all modified node and edges.
                                it first gathers all vertex from the edge list and create a list of all nodes
                                Then it prepare the list needed for dijkstra: Q, pred, dist. As it use heapq, the
                                time complexity of push and pop only cost O(log L).
                                Inorder to achieve the complexity, It followed the priority queue approach to push the
                                adjacent node of u into Q, for each relaxed edge.  It pushes the starting node,
                                then it goes into the while loop.
                                It pops from Q for the node to process, since there might be outdated node inside Q, it
                                ignores it to avoid issues.  Then the for loop will only run while using an if statement
                                to check is the edge starts from the one that it is processing.  The edge get relax and
                                pushed into Q, and update the related value at pred and dist.
                                Once the loop ended, there might be chance that it ends at the T3 lane or normal lane of
                                the last note, It checks which one it is ended and grab the shortest path to that node with
                                shortest_path_retrieval(), then return.

        Input:  graph:  that modified graph that create before it called dijkstra.
                start:  indicate which nodes is the starting nodes.

        Output: result: the path that leads to the end with the shortest time.

        Time complexity:        O(R log L)
        Aux space complexity:   O(L)
    '''
    locations = []
    for edge in graph:                                  # O(R), get the amount of vertex from all edges
        if edge[0] not in locations:
            locations.append(edge[0])
        if edge[1] not in locations:
            locations.append(edge[1])

    Q = []
    pred = [None] * len(locations)                      # O(L)
    dist = [float('inf')] * len(locations)              # O(L)
    dist[start*2+1] = 0
    heapq.heappush(Q, (dist[start*2+1], start*2+1))             # O(log L)

    while len(Q) != 0:                                  # O(L)
        u = heapq.heappop(Q)                            # O(log L), get the min_node
        if u[0] > dist[u[1]]:                           # check is it out of date, yes -> next loop
            break
        u = u[1]
        for edge in graph:                              # O(R)
            if edge[0] == u:                            # if the edge start from u, only nodes that adjacent to this will go through
                v = edge[1]                             # for graph that not all nodes are connect to each other, those that arent adjacent are ignored, therefore O(R)
                current_route_time = dist[u] + edge[2]  # relax the nodes
                alt_route_time = dist[v]
                if current_route_time < alt_route_time:
                    dist[v] = current_route_time
                    heapq.heappush(Q, (dist[v], v))     # O(log L), put into Q with newly updated node
                    pred[edge[1]] = u

    min_dist = min(dist[end*2], dist[end*2+1])              # O(1)
    if min_dist == dist[end*2]:
        ending_in = end * 2                                 # T3
    else:
        ending_in = end * 2 + 1                             # normal lane
    result = shortest_path_retrieval(pred, ending_in)       # O(L)
    return result


def shortest_path_retrieval(pred, target):
    '''
        Function description:   This function takes the pred array and return the path that created the min.
        Approach description:   This function take pred array as input. It knew where it is ending (target param)
                                    and append. Given that start != end, it will at least take 2 steps for both start
                                    and end node.
                                Then it goes into the while loop that checks is there another node that leads to the
                                    latest node (i.e. the last node of the result), if yes -> append, no -> end loop.
                                This method track at the end, therefore it need to reverse the list to the start node is
                                at the front.
                                Before the dijkstra is called at optimalRoute(), we modified the graph.  In order to
                                    display the path in original form, it needs to reverse the modification.  Hence,
                                    goes through another loop that reverse all modified nodes number. Note that we split
                                    the nodes into two at first, the nodes that switched to T3 lane will have the identical
                                    number.  The function check if previous node is the same and just append once only.
                                It does not make sense if the previous node and the next node is the same, otherwise the
                                    node return to itself but there is no way to do so.
                                And it returns the final result by using the numbering of the original graph.

        Input:  pred:           the steps array that used to track back the path that it come from.
                target:         the end of the trip, that start of tracking backwards.

        Output: update_result:  returns the final result by using the numbering of the original graph.

        Time complexity:        O(3L) = O(L)
        Aux space complexity:   O(L)
    '''
    result = [target]
    result.append(pred[target])
    while pred[result[len(result) - 1]] is not None:    # O(L), at most visited all nodes
        result.append(pred[result[len(result) - 1]])
    result.reverse()                                    # O(L), the list is track backwards

    update_result = []
    for step in result:                                 # O(L), turn the nodes number to original form
        if step % 2 == 0:  # is even, T3
            renew = int(step / 2)
        else:
            renew = int((step - 1) / 2)
        if len(update_result) == 0 or renew != update_result[len(update_result) - 1]:
            update_result.append(renew)

    return update_result


def clamp(x, lower_bound, upper_bound):
    '''
    Function description:   This function return a clamped result of the input x, if x is not between the lower_bound or upper_bound,
                            mainly used for Q2 list not exceeding the range

    Approach description:   x first put through min(x, upper_bound), min will return the smallest value.
                            (i.e. if x is beyond the upper_bound, upper_bound will be returned instead)
                            min() has the complexity of O(n), where n is the input size.
                            Here, I am only comparing 2 int item, therefore the input size is 2 and the complexity will be O(2).
                            Then, that value returned from min() (let that value be min_r) will pass to max(lower_bound, min_r).
                            Again, only comparing 2 int item here, same as min, the complexity will be O(2).

    Input:  x:              the value that will be clamped
            lower_bound:    the minimum value it will return
            upper_bound:    the maximum value it will return

    Output: the clamped value that is between lower_bound and upper_bound

    Time complexity:        O(2) + O(2) = O(1)
    Aux space complexity:   O(1)
    '''
    return max(lower_bound, min(x, upper_bound))


def select_sections(arr):
    '''
    Function description:   This function return the optimal route with the lowest travel time.
    Approach description:   This function make use of Dynamic Programming approach. For each slot (except for all
                                element in the first row), it calculates the smallest value at that slot that is
                                 reachable (adjacent) in previous row. The value of [n][m] + the slot of the previous
                                 rows will slowly fill up the whole memo matrix array.
                            During the selection of the smallest value to be put in, those value that is not optimal
                                will not be selected. This Dynamic Programming approach avoid brute forcing all
                                combination, reducing time.
                            Once the memo is created, there will be at least one minimum element in the last row.
                            Based on the memo, the minimum value and the route will be retrieved.

    Given n is the number of elements in the input list:
                The dynamic programming uses a memo matrix array, which will be filled slot by slot. It takes O(nm).
                Then it retrieve the route from path_retrieval() which take O(nm).

    Input:      arr: the matrix array contains the occupancy of each section.
    Output:     [min_result, path]:
                    min_result: the minimum occupancy possible in this matrix array
                    path: the section that achieve the mim_result

    Time complexity:        O(nm) + O(nm) = O(nm)
    Aux space complexity:   O(nm) + O(n) (from section_retrieval()) = O(nm)
    '''
    memo = []
    for n in range(len(arr)):
        row = []
        for m in range(len(arr[n])):
            if n == 0:  # the first row does not have previous row to be calculated on
                row.append(arr[n][m])  # It takes the value from arr to start
            else:
                lowest = min(memo[n - 1][clamp(m - 1, 0, len(memo[n - 1]) - 1)], memo[n - 1][m],
                             memo[n - 1][clamp(m + 1, 0, len(memo[n - 1]) - 1)])  # 3 elements, O(3)
                row.append(lowest + arr[n][m])
        memo.append(row)

    minimum_total_occupancy = min(memo[len(memo) - 1])
    sections_location = section_retrieval(memo)  # O(nm)

    # print([minimum_total_occupancy,  sections_location])
    return [minimum_total_occupancy, sections_location]


def section_retrieval(memo):
    ''' n = rows, m = column
    Function description:   This function takes the memo array and return the path that created the min.
    Approach description:   This function goes at the end of the array's row, then go through a minimum finding
                                function to locate the min weight slot.
                            Only the first iteration need to goes through the whole column length of the last row
                                since there is no further rows to determine which three slot to limit for tracing
                                the route.
                            Every slot in the memo array can only be added up from one of the three column from the
                                previous column, that is the same or adjacent rows.
                            It has to start at the end of all rows, if it starts at the front and seek for the lowest
                                value at the next row, the lowest value among those 3 slot might not lead to the
                                smallest path at the end since the ongoing numbers might add up more than other paths.
                            By doing it backwards, it could knows which slot leads to the shortest path ended.
                            Since the memo creating function put a value based from arr[n][m] + the smallest value of
                                those three slot, the path tracking finds the smallest among those 3 (same or adjacent).
                            The upper_bound and lower_bound limits the only possible range of those three slots.
                            When it finds the correct slot, it set the range for the previous column (next iteration).
                            The function keeps going backwards and following the which possible slot from previous rows
                                it came from and append that location into path array.
                            It goes backwards makes the path append backwards as well. So it reverse() the list as output.
                            If there is two optimal route (i.e. same value at the end), it will just choose one way to go.
                            It does not matter which path it choose since both path leads to the same min value.

    Given n is the number of elements in the input list:
                            It goes through each row (n), then it compare the possible path from those three columns
                            in the previous rows, but it has to locate the destination which needs to check at most all
                                column (m).
                            At last it reverse() the list, reverse cost O(n).

    Input:                  memo: a matrix array memo created by the memo creating function.

    Output:                 sections_location: an array that contains all the steps taken that leads to the minimum weight.

    Time complexity:        O(nm) + O(n) = O(nm)
    Aux space complexity:   O(n): the path need to store all chosen (i, j) where n == len(memo)
    '''
    sections_location = []
    next_upper = len(memo[len(memo) - 1])  # upper & lower bound for the last column
    next_lower = 0
    for n in range(len(memo) - 1, -1, -1):  # starting from the last column (n), and slowly trace backwards, O(n)
        min_temp = float("inf")
        upper_bound = next_upper  # apply the bound that can be reached from the previous column
        lower_bound = next_lower
        for m in range(lower_bound,
                       upper_bound):  # at most 3 position that could reach this slot (adjacent) except the first iteration
            if memo[n][m] < min_temp:  # finding the min value and its location O(m)
                min_temp = memo[n][m]
                location = (n, m)
                next_upper = clamp(m + 2, 0, len(memo[n]))  # limit the next search bound that adjacent to this slot
                next_lower = clamp(m - 1, 0, len(memo[n]) - 1)  # and not exceeding the list range using clamp()
        sections_location.append(location)
    sections_location.reverse()  # the list starts at the end, it has to be reversed
    return sections_location


if __name__ == '__main__':
    start = 5
    end = 4

    # the location where there are potential passengers
    passengers = [2, 1]
    # the roads represented as a list of tuple
    roads = [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
             (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20), (5, 0, 1, 1)]

    # your function should return the optimal route
    optimalRoute(start, end, passengers, roads)

    # Q2
    occupancy_probability = [
        [31, 54, 94, 34, 12],
        [26, 25, 24, 16, 87],
        [39, 74, 50, 13, 82],
        [42, 20, 81, 21, 52],
        [30, 43, 19, 5, 47],
        [37, 59, 70, 28, 15],
        [2, 16, 14, 57, 49],
        [22, 38, 9, 19, 99]]

    # select_sections(occupancy_probability)
