def mine_frequent_subgraphs_helper(frequent_subgraphs):
  # where_code_output = []
  where_code_output = {}
  
  # print('helper', frequent_subgraphs)

  for i in range(len(frequent_subgraphs)):
      lines = frequent_subgraphs[i].split('\n')
      for line in lines.copy():
          if line and line[0] == "t": 
            tree_index = int(line.split('#')[1].strip())
            # print('tree indexx in helper ', tree_index)  
          elif not line or line[0] not in ["v", "e"]:
              if line.startswith('where:'):
                where_str = line[8:-1]      
                where_arr = where_str.split(', ')
                where_arr = [int(val) for val in where_arr]
                # print(where_arr)
                # where_code_output.append(where_arr)
                where_code_output[tree_index] = where_arr

                # print('where', where_code_output)
              lines.remove(line)       
      frequent_subgraphs[i] = '\n'.join(lines)
  return frequent_subgraphs, where_code_output