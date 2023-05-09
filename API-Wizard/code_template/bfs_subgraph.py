"""#BFS Subgraphs algorithm"""

# Define a function named 'parallel_bfs' that takes in three arguments: two adjacency lists (adj_list_lg and adj_list_sm) and a starting node.


def parallel_subgraph_bfs(adj_list_lg, adj_list_sm, start_node, lg_v, sm_v):
    # Initialize two empty sets 'visited_lg' and 'visited_sm', and two empty queues 'queue_lg' and 'queue_sm'.
    visited_lg = set()
    visited_sm = set()

    # Add the starting node to both 'visited_lg' and 'visited_sm', and to 'queue_lg' with an empty string,
    # and to 'queue_sm' with a node 0 and an empty string.
    queue_lg = deque([(start_node, '')])
    queue_sm = deque([(0, '')])
    visited_lg.add(start_node)
    visited_sm.add(0)

    while len(queue_sm) > 0:
        # print('before pop queue_lg',queue_lg)
        # print('before pop queue_sm',queue_sm)
        # Check if 'queue_lg' is empty, and if so, return False. Otherwise, dequeue the first node from both 'queue_lg' and 'queue_sm'.
        if (len(queue_lg) == 0):
            return False

        node1 = queue_lg[0]
        node2 = queue_sm[0]

        # Check if the names of the nodes in 'lg_v' and 'sm_v' dictionaries are the same, and if not, return False.
        # if(lg_v[node1[0]] != sm_v[node2[0]]): return False;
        if (lg_v[node1[0]] != sm_v[node2[0]]):
            # print('not equal will pop from large only 1')
            node1 = queue_lg.popleft()
            continue

        # check if the labels of the nodes are the same, and if not, return False.
        # if(node1[1] != node2[1]): return False;
        elif (node1[1] != node2[1]):
            # print('not equal will pop from large only 2')
            node1 = queue_lg.popleft()
            continue

        else:
            node1 = queue_lg.popleft()
            node2 = queue_sm.popleft()
            # print('after pop queue_lg',queue_lg)
            # print('after pop queue_sm',queue_sm)

        # Extract the node numbers from node1 and node2
        node1 = node1[0]
        node2 = node2[0]

        # For each neighbor of node1 in the larger graph, add it to 'queue_lg' and 'visited_lg' if it has not already been visited.
        for neighbor in adj_list_lg[node1]:
            if neighbor[0] not in visited_lg:
                visited_lg.add(neighbor[0])
                queue_lg.append((neighbor[0], neighbor[2]))

        # For each neighbor of node2 in the smaller graph, add it to 'queue_sm' and 'visited_sm' if it has not already been visited.
        for neighbor in adj_list_sm[node2]:
            if neighbor[0] not in visited_sm:
                visited_sm.add(neighbor[0])
                queue_sm.append((neighbor[0], neighbor[2]))

    # Return True if the while loop is exited, which indicates that all nodes in the smaller graph have been visited and matched to nodes in the larger graph.
    # so indicates the sammler graph is a subgraph
    return True


def parallel_bfs_supgraphs_helper(lg_v, sm_v, lg_edges, sm_edges):
    search_string = sm_v[0]
    found_search = False
    foundV_key = 0

    # Looping through all nodes in the larger graph and searching for a matching node
    # to check the possibility of finding a subgraph
    for key, value in lg_v.items():
        if value == search_string:
            foundV_key = key
            found_search = parallel_subgraph_bfs(
                lg_edges, sm_edges, foundV_key, lg_v, sm_v)
            if (found_search):
                break

    # If no matching node was found or the graphs are not subgraphs, return
    if (not found_search):
        # print(f'The Two graphs are NOT subgraph')
        return False
    else:
        # print(f'found a subgraph')
        return True
