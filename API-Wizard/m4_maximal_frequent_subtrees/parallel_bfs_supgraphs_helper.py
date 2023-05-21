from m4_maximal_frequent_subtrees.parallel_subgraph_bfs import parallel_subgraph_bfs

#This function utilizes parallel BFS to determine if one graph is a subgraph of another
def parallel_bfs_supgraphs_helper(lg_v, sm_v, lg_edges, sm_edges ):
    # Set the search_string to the first vertex in the small graph
    search_string = sm_v[0]
    found_search = False
    foundV_key= 0

  # Looping through all nodes in the larger graph and searching for a matching node 
  #to check the possibility of finding a subgraph
    for key, value in lg_v.items():
      if value == search_string:
          foundV_key =key
          found_search = parallel_subgraph_bfs(lg_edges,sm_edges,foundV_key, lg_v, sm_v)
          if(found_search): break
          
    # If no matching node was found or the graphs are not subgraphs, return
    if (not found_search) :
      #The Two graphs are NOT subgraphs
      return False
    else:
      #found a subgraph
      return True