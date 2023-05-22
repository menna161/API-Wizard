from collections import deque
import re

#this function performes a parallel bfs on both the large and
# small tree to determine if they are subgraphs of each other or not but
#  taking the nodes with placeholders into consideration
def parallel_bfs_placeholder(lg_v, sm_v, adj_list_lg, adj_list_sm, start_node):    
    # Initialize two empty sets 'visited_lg' and 'visited_sm', and two empty queues 'queue_lg' and 'queue_sm'.
    visited_lg = set()
    visited_sm = set()

    # Add the starting node to both 'visited_lg' and 'visited_sm', and to 'queue_lg' with an empty string, 
    # and to 'queue_sm' with a node 0 and an empty string.
    queue_lg = deque([(start_node,'')])
    queue_sm = deque([(0,'')])
    visited_lg.add(start_node)
    visited_sm.add(0)

    tmp_score = {} 
    vertex_numbers = []
    placeholder_n = 0
    
    while len(queue_lg) > 0 :
        isPlaceholder = False   
        # Check if 'queue_lg' is empty, and if so, return False. Otherwise, dequeue the first node from both 'queue_lg' and 'queue_sm'.

        if(len(queue_sm) == 0):
            queue_sm.clear()
            queue_sm = deque([(0,'')])
            return tmp_score , vertex_numbers
        
        node1 = queue_lg[0]
        node2 = queue_sm[0]
        # Check if the vertex in 'queue_sm' is a placeholder or a regex pattern.
        if('PLACEHOLDER' in  sm_v[node2[0]] or '(.*)' in sm_v[node2[0]]):
          isPlaceholder = True
          sm_v[node2[0]] = sm_v[node2[0]].replace('PLACEHOLDER', '(.*)')
          tmp_score['placeholder'+str(placeholder_n)] = {}
          
      # Match the pattern in 'sm_v' with the value in 'lg_v'
        match = re.findall( sm_v[node2[0]], lg_v[node1[0]])
        
        # If no match is found, dequeue the first node from 'queue_lg' and continue the loop.
        if( not match):    
          node1 = queue_lg.popleft()
          continue

        else: 
           # If the vertex is a placeholder, store the match in 'tmp_score' and update the placeholder count.
          if isPlaceholder:
            tmp_score['placeholder'+str(placeholder_n)][match[0]] = 1
            placeholder_n = placeholder_n+1
            vertex_numbers.append(node2[0])

          node1 = queue_lg.popleft()
          node2 = queue_sm.popleft()
      

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
    #so indicates the sammler graph is a subgraph
    if(len(queue_sm) != 0): return None ,None

    return tmp_score ,vertex_numbers