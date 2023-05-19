from collections import deque
import re
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
        # print('before pop queue_lg',queue_lg)
        # print('before pop queue_sm',queue_sm)
        # Check if 'queue_lg' is empty, and if so, return False. Otherwise, dequeue the first node from both 'queue_lg' and 'queue_sm'.

        # print('queue_sm', queue_sm)
        if(len(queue_sm) == 0):
            queue_sm.clear()
            queue_sm = deque([(0,'')])
            # print("vertex_numbers",vertex_numbers)
            return tmp_score , vertex_numbers
        
        node1 = queue_lg[0]
        node2 = queue_sm[0]
        # print('node1',lg_v[node1[0]])
        # print('node1 num',node1[0])
        # print('node2',sm_v[node2[0]])
        # print('node2',node2[0])
        # print('adj_list_lg', adj_list_lg)
        # print('adj_list_sm', adj_list_sm)

        # print('lg_name',lg_v[node1[0]])
        # print('sm_name',sm_v[node2[0]])
        # node1 = queue_lg.popleft()
        # node2 = queue_sm.popleft()

        # Check if the names of the nodes in 'lg_v' and 'sm_v' dictionaries are the same, and if not, return False.
        # if(lg_v[node1[0]] != sm_v[node2[0]]): return False;

        if('PLACEHOLDER' in  sm_v[node2[0]] or '(.*)' in sm_v[node2[0]]):
          isPlaceholder = True
          sm_v[node2[0]] = sm_v[node2[0]].replace('PLACEHOLDER', '(.*)')
          tmp_score['placeholder'+str(placeholder_n)] = {}
          
      
        match = re.findall( sm_v[node2[0]], lg_v[node1[0]])
        
        if( not match):    
          # print('not equal will pop from large only 1')
          node1 = queue_lg.popleft()
          # print('if queue_lg',queue_lg)
          # print('if queue_sm',queue_sm)
          continue

        
        #check if the edges name are the same
        # elif(node1[1] != node2[1]):
        #     # print('not equal will pop from large only 2')
        #     node1 = queue_lg.popleft()
        #     # print('else queue_lg',queue_lg)
        #     # print('else queue_sm',queue_sm)
        #     continue;
            
        else: 

          # print('matchhhh', match[0])
          # print('isPlaceholder', isPlaceholder)
          if isPlaceholder:
            # print('added in temp_score ', placeholder_n, match[0])
            tmp_score['placeholder'+str(placeholder_n)][match[0]] = 1
            placeholder_n = placeholder_n+1
            vertex_numbers.append(node2[0])

          node1 = queue_lg.popleft()
          node2 = queue_sm.popleft()
          # print('after pop queue_lg',queue_lg)
          # print('after pop queue_sm',queue_sm)

        # Extract the node numbers from node1 and node2
        node1 = node1[0]
        node2 = node2[0]

        # For each neighbor of node1 in the larger graph, add it to 'queue_lg' and 'visited_lg' if it has not already been visited.
        # print('adj_list_lg[node1]', adj_list_lg[node1])
        # print('adj_list_sm[node2]', adj_list_sm[node2])

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
    # print('queue_sm ', queue_sm)
    if(len(queue_sm) != 0): return None ,None

    # print("vertex_numbers",vertex_numbers)
    return tmp_score ,vertex_numbers