# code by 32868901, Yin Lam LO for FIT2001 A2, 2023 S1

# below code for Q1

def maxThroughput(connections, maxIn, maxOut, origin, targets):
    '''
            Function description: This function based on Ford-Fulkerson algorithm to return max flow of a given graph
            Approach description: To work easier, the connection list are modified to connections_with_flow with flow as
                                    one of the element.  parent list is used to track the path, the path is tracked
                                    during BFS. The loop will run until there is no available path to augment the flow.
                                    During the loop, a new dest and parent list will be calculated, and each loop
                                    calculate the max flow of that path. First it calculates the max flow of that path
                                    by backtracking with parent list and add it to max flow.  Then, since there is a
                                    successful flow, the capacity of the edges, maxIn, and maxOut need to be updated.
                                    After it was updated, it runs BFS again to find another path.  if it returns another
                                    int (i.e. another reachable target), it continues until no more path is found.
                                    Otherwise the loop ends and return the cumulated max flow.

            Input: connections: graph_of_edges
                   maxIn: list of maximum input of vertex
                   maxOut: list of maximum Output of vertex
                   origin: where the flow start
                   targets: where the flow could go to

            Output: max_flow: maximum flow of going to all the targets from origin

            Time complexity:    O(V+EV+E(3EV)) = O(VE^2)
            Aux space complexity: O(E+V) = O(V)
    '''

    connections_with_flow = []  # recreate the graph with flow as one of the element
    for edge in connections:    # u, t, flow, capacity                  O(V)
        connections_with_flow.append([edge[0], edge[1], 0, edge[2]])

    parent = [None] * len(get_vertices(connections))    # array to store path
    max_flow = 0

    dest = bfs(connections_with_flow, origin, targets, parent, maxIn, maxOut)  # O(EV)
    # if it finds a path to any of the targets, until the all edges was processed, do below
    while dest is not None:
        # following the parent array, process as parent[s] (where the edge starts) and s (edge ends) pairs, O(E)

        path_flow = float("inf")
        s = dest
        while s != origin:  # search for max flow of the path avoiding any bottleneck  O(V)
            edge = find_edge(connections_with_flow, parent[s], s)   # O(E)
            path_flow = min(path_flow, edge[3] - edge[2], maxOut[parent[s]], maxIn[s])
            s = parent[s]   # for next
        max_flow += path_flow

        v = dest
        while v != origin:  # change the capacity according to the flow         O(V)
            edge = find_edge(connections_with_flow, parent[v], v) # O(E)
            edge[2] += path_flow  # add to flow
            maxOut[parent[v]] -= path_flow  # flow lead to lower maxOut for parent, and lower maxIn for child
            maxIn[v] -= path_flow
            v = parent[v]   # for next

        dest = bfs(connections_with_flow, origin, targets, parent, maxIn, maxOut)  # O(EV)

    return max_flow

def find_edge(connections, from_, to_):  # O(E)
    '''
            Function description: For searching a specific edge among all the edges.
            Approach description: for loop search, to reduce repetition code and make it easier to read.

            Input:  connections: graph_of_edges getting search through
                    from_ : used to find that edge that start with this vertex
                    to_ : used to find that edge that end with this vertex

            Output: edge that match above conditions

            Time complexity: O(E)
            Aux space complexity: O(1)
    '''
    for edge in connections:
        if edge[0] == from_ and edge[1] == to_:
            return edge

def get_vertices(graph_of_edges) -> list:
    '''
            Function description: return the list of vertices from a graph of edges
            Approach description: This function will be commonly used, to avoid repetition, this function is implemented
                                    for each edge in graph_of_edges, check all start vertex and end vertex.
                                    if that vertex is not counted yet, it will be added to vertices.
                                    after the count, vertices will be returned.

            Input:  graph_of_edges: given graph
            Output: list of vertices

            Time complexity: O(E(V+V)) = O(EV)
            Aux space complexity: O(V), all vertices
    '''
    vertices = []
    for edge in graph_of_edges:  # O(E)
        if edge[0] not in vertices:  # O(V)
            vertices.append(edge[0])
        if edge[1] not in vertices:  # O(V)
            vertices.append(edge[1])
    return vertices

def bfs(connections, origin, targets, parent, maxIn, maxOut) -> int:  # O(EV)
    '''
            Function description: Breadth First Search, for searching available path to augment the flow
            Approach description: queue stores the vertices that waiting to be searched with adjacent vertex following
                                    the edges.  Start with the origin, for every vertex we tracked, we marked it as
                                    visited using visited[].  The vertex from the queue will be popped.  If that vertex
                                    have reached its max output, it means it cannot output anymore and no more flow can
                                    be increase through its edges.  This vertex will be ignored.  Otherwise, every edge
                                    that starts from this vertex will be checked is it capable of passing the flow.
                                    When it is capable, it will be appended to queue to be waited to visit and be marked
                                    in parent for the path relations.  Once all vertices was checked, if any of the
                                    targets was visited, it will be returned.  If no target was founded, None will be
                                    returned.

            Input:  connections: modified graph of edges with flow integrated as one of the element
                    origin: where the flow starts
                    targets: destination that the flow needs to go
                    parent: parent list passed from maxThrough() to track its path
                    maxIn: maximum input for each vertex
                    maxOut: maximum output for each vertex

            Output: target | None: found path that leads to one of the targets, None if cannot be reached

            Time complexity:        O(EV) + O(EV) + O(E) = O(EV)
            Aux space complexity:   O(V), from visited[], largest size list in this method
    '''

    # for define visited list sizes
    vertices = get_vertices(connections)  # O(EV)

    visited = [False] * len(vertices)
    queue = []
    queue.append(origin)
    visited[origin] = True

    while queue:  # O(V)
        current = queue.pop(0)
        if maxOut[current] == 0:  # cant output more if maxOut is reached, ignore this vertex
            continue
        for edge in connections:  # for all edge that starts from current          O(E)
            if edge[0] is current:
                if not visited[edge[1]] and edge[2] < edge[3] and maxIn[edge[1]] > 0:
                    # when edge have a non-visited vertex, still got spare flow, and ongoing vertex not reached maxIn
                    queue.append(edge[1])
                    visited[edge[1]] = True
                    parent[edge[1]] = current   # set what vertex lead to this vertex

    # return the found target, else return none if no target can be reached
    for target in targets:  # O(E)
        if visited[target]:
            return target
    return None

# end of code Q1



# below code for Q2

def locate(alphabet) -> int:
    '''
                Function description: This function return the position of the array according to the alphabetic order
                Approach description: Just for loop checking which alphabet is the same and that location and return it

                Input: alphabet: the alphabet that needs to find the correspondence position inside the list for nodes
                Output: max_flow: The correspondent slot of the list

                Time complexity:    O(len(alphabets)) = O(27) = O(1)
                Aux space complexity: O(27) = O(1)
    '''
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "$"]
    for index in range(len(alphabets)):
        if alphabet == alphabets[index]:
            return index
    return None # not in list, should be here

class Node:
    '''
    Node class for handling all the subtrie implementation
    the ground work of the cattrie, which includes some key information that pre-processed to be used in auto-complete
    the detail of how this class will be used will be in the Catstrie class
    '''
    def __init__(self, letter: str, freq = 1, depth = 0):
        """
        :param letter:  the letter of the node
        :param freq:    the frequency of this letter node appeared among the sentences, assume it had appeared for one
                        when created, default value = 1
        :param depth:   the depth of the trie (length of sentence) where is node is, default = level 0

        attrubute:
            letter      # the letter itself
            freq        # the times that this sequence have appeared in sentences
            depth       # the depth of this section of this subtrie, the length of the sentence
            max_freq    # be used in after the trie has built, mark down the max freq and max depth of this subtrie
            max_depth   # both are used for auto complete decision
            lst         # where the next nodes go, 26 alphabet + end "$" = 27

        Time complexity:    O(27) = O(1)
        Aux space complexity: O(27) = O(1)
        """
        self.letter = letter
        self.freq = freq
        self.depth = depth
        self.max_freq = 0
        self.max_depth = 0
        self.lst = [None] * 27

    def add_freq(self):
        '''
                Function description: add one freq to the current node
                Time complexity:    O(1)
                Aux space complexity: O(1)
        '''
        self.freq += 1

    def get_subtrie(self, letter: str): # return node or none
        """
        :param letter: the letter subtrie that we wanted
        :return: the subtrie that starts with this letter of this node
        Time complexity:    O(1)
        Aux space complexity: O(1)
        """
        return self.lst[locate(letter)]

    def add_subtrie(self, letter: str):
        """
        create a node that with connects to this alphabet if it havent exist, otherwise return the existing one.
        :param letter:  the node's letter that we wanted
        :return:    the found node, or the node that we just created.
        Time complexity:    O(1)
        Aux space complexity: O(1)
        """
        if self.lst[locate(letter)]:
            self.lst[locate(letter)].add_freq()
            return self.lst[locate(letter)]
        else:
            new_node = Node(letter, depth=self.depth+1)
            self.lst[locate(letter)] = new_node
            return self.lst[locate(letter)]

# The CatsTrie class structure
class CatsTrie:
    def __init__(self, sentences):      # O(NM)
        '''
            Function description: This function built a trie based on the given sentences.
            Approach description: For each letter in every sentences, it do the below things:
                                    first it setting up the root node, then convert the sentence into a tree.
                                    current variable will be the node it is processing, hence "current".
                                    the node's frequency will increment one to indicate the count that this node has
                                    appeared as part of the sentence.  The for each letter in sentence will be created
                                    with a new node and the letter after that will be placed at its list. After a
                                    sentence is done, a "$" node will be added (see below anchor 1) to signify the end
                                    of the sentence.  The trie of this sentence is completed, inorder to make it capable
                                    for auto-complete, Its going to update each node of this sentence create and update
                                    the max_freq and max_depth for decision making for the question giving conditions.
                                    Since max_freq and max_depth is the same the end node, this two variable will be
                                    compared for the existing value of that node for the larger one.  All the
                                    pre-processing of the trie is done.

                                    Add the origin and end node will make the time complexity increase by 2, but with
                                    bigO, O(Y+2) = O(Y). Therefore it is still inside the complexity range.

            Input:  sentences: list of sentence that needs to be processed

            Time complexity:        O(NM), for each sentence(N), each letter(M)
            Aux space complexity:   O(1), the origin node
        '''
        # for each letter in every sentences
        self.origin = Node("$", 0)
        for sentence in sentences:      # O(N) N: len(sentences)
            self.origin.add_freq()      # increment the frequency
            current = self.origin       # setup the start node
            for letter in sentence:     # O(M) M: len(longest_sentence)
                new = current.add_subtrie(letter)   # if node of this letter existed, return it, else create a new node
                current = new                       # move on to next node
            new = current.add_subtrie("$")  # anchor 1 for description, end of the sentence
            # end of building the trie, new: the end node of the sentence

            # using the info of the end sentence node, update freq and depth
            current = self.origin       # for origin node
            current.max_freq = max(new.freq, current.max_freq)
            current.max_depth = max(new.depth, current.max_depth)
            for letter in sentence:     # for all nodes in a sentence
                current = current.get_subtrie(letter)
                current.max_freq = max(new.freq, current.max_freq)
                current.max_depth = max(new.depth, current.max_depth)
            current = current.get_subtrie("$")  # for end node
            current.max_freq = max(new.freq, current.max_freq)
            current.max_depth = max(new.depth, current.max_depth)

    def autoComplete(self, prompt):
        '''
            Function description: This function auto complete based on the given prompt and the pre-processed trie
            Approach description: To auto complete, it first traces to the node where the prompt ends. For each letter
                                    in prompt, go next node. If such node does not exist, it cannot be auto completed,
                                    return none. When that part is done, we are at the node when the prompt ends.
                                    Then the next node is find among all nodes connected with the current node, by going
                                    through all nodes with a for loop. When it reached an end node. the auto complete
                                    is done and return this result.


            Input:  given prompt
            Output: the auto completed result based on the given prompt

            Time complexity:        O(X+Y)
            Aux space complexity:   O(1)
        '''
        result = ""  # the string to be auto complete

        # find the latest node up to the last letter from prompt
        current = self.origin
        for letter in prompt:                   # max the prompt is whole sentence, O(X)
            nxt = current.get_subtrie(letter)
            if nxt is None: # no such prefix
                return None
            result += nxt.letter    # filling it to the result
            current = nxt

        suggested = Node("$", 0, 0) # dummy node for comparison, for finding the suitable next for to be auto completed
        while True:                         # for each node in the next node list that matches.
                                            # contiune until it reach the end node (the longest sentence), O(Y)
            for node in current.lst:        # for each connected node in current node, find the most suitable node
                if node is not None:        # by the condition below
                    if node.max_freq == suggested.max_freq:     # if same max freq
                        if node.max_depth < suggested.max_depth:    # compare depth (smaller string has priority)
                            suggested = node
                            current = node
                    elif node.max_freq >= suggested.max_freq:   # if the node have higher max_freq it has priority
                        suggested = node
                        current = node
            if suggested.letter != "$":     # only auto complete with letters, not end of sentence indicator
                result += suggested.letter

            suggested = Node("$", 0, 0)     # for next loop
            if current.letter == "$":       # if its processing the end node, end loop
                break
        return result

# end of code Q2
