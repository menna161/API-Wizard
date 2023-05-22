from helpers.representing_trees import representing_trees
import re
from globals import score
from .parallel_bfs_placeholder import parallel_bfs_placeholder

#This function utilizes parallel BFS to determine if one graph is a subgraph of another
def placeholder_bfs_helper(lgGraph, smGraph ,new_template ):
    lg_v = {}
    sm_v = {}
    merged_scores = {}
    merged_vertex_numbers = []
    

    lg_v, sm_v, lg_edges, sm_edges = representing_trees(lgGraph, smGraph)


    #search for the first occurence of the node
    search_string = sm_v[0]
    found_search = False
    foundV_key= 0

    if(new_template):
      i = 0
      for key, value in sm_v.items():
        if 'PLACEHOLDER' in value:
          # print('value' , value)
          score['placeholder'+str(i)] = {}
          i = i+1
      new_template= False
  # Looping through all nodes in the larger graph and searching for a matching node 
  #to check the possibility of finding a subgraph
    
    for key, value in lg_v.items():
      matches = re.findall( re.escape(value), search_string)
      if  matches:
        for match in matches:

          foundV_key =key
          tmp_score , vertex_numbers = parallel_bfs_placeholder(lg_v, sm_v,lg_edges,sm_edges,foundV_key)

          if(tmp_score is not None):            
            found_search = True
            merged_vertex_numbers = vertex_numbers
            for key, values in tmp_score.items():
              try:
                merged_scores[key].update(tmp_score[key])
              except:
                merged_scores[key] = {}
                merged_scores[key].update(tmp_score[key])
            
          
    if ( found_search) :
      for key, values in merged_scores.items():
        for sub_key, sub_value in values.items():
          if key in score and sub_key in score[key]:
              score[key][sub_key] = score[key][sub_key] + 1 if sub_key in merged_scores[key] else score[key][sub_key]
          else:
              score[key][sub_key] = 1
      return score ,merged_vertex_numbers
    else:
      print('##############did not find the pattern in the big tree')
      return None ,None
