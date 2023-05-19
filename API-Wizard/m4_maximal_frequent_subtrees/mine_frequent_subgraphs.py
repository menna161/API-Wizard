import re
from m4_maximal_frequent_subtrees.mine_frequent_subgraphs_helper import mine_frequent_subgraphs_helper
from helpers.representing_trees import representing_trees
from m4_maximal_frequent_subtrees.parallel_bfs_supgraphs_helper import parallel_bfs_supgraphs_helper

def mine_frequent_subgraphs(frequent_subgraphs ):
  lg_v = {}
  sm_v = {}


  frequent_subgraphs, where_code_output = mine_frequent_subgraphs_helper(frequent_subgraphs)


  frequent_subgraphs.sort(key=lambda x: len(x))

  sml_pointer = 0
  lg_pointer = len(frequent_subgraphs) - 1

  while sml_pointer < len(frequent_subgraphs):
    sml_pointer_temp= sml_pointer
    while sml_pointer < lg_pointer:
        
        lg_v, sm_v, lg_edges, sm_edges = representing_trees(frequent_subgraphs[lg_pointer], frequent_subgraphs[sml_pointer])
        
        if parallel_bfs_supgraphs_helper(lg_v, sm_v, lg_edges, sm_edges ):
          
          frequent_subgraphs.pop(sml_pointer)
          # where_code_output.pop(sml_pointer)
          lg_pointer = len(frequent_subgraphs) - 1
          
        else:
          # sml_pointer += 1
          lg_pointer -= 1
    sml_pointer = sml_pointer_temp+1
    lg_pointer = len(frequent_subgraphs) - 1

  # frequent_subgraphs, where_code_output = mine_frequent_subgraphs_helper(frequent_subgraphs)
  filtered_where_code_output = []
  for fg  in frequent_subgraphs:
    # print('final frequent subgraphsss ',fg )

    match = re.search(r"t # (\d+)", fg)
    if match:
      index = int(match.group(1))
      # print('index of where t #', index)
      filtered_where_code_output.append(where_code_output[index])



  # return frequent_subgraphs, where_code_output
  return frequent_subgraphs, filtered_where_code_output