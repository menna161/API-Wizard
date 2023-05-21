
#This is a helper function to store the wheres of each tree
#The wheres is a list of indices indicating where did the tree come from the orignial code snippets given as input
#E.g. where_code_output of tree 1 =[0,1,2] , the tree came from code snippet 0 ,1 & 2.

def mine_frequent_subgraphs_helper(frequent_subgraphs):
    # Dictionary to store the 'where' code output
    where_code_output = {}

    # Iterate over each frequent subgraph
    for i in range(len(frequent_subgraphs)):
        lines = frequent_subgraphs[i].split('\n')
        
        for line in lines.copy():
            if line and line[0] == "t":
                # Extract the tree index from the 't' line
                tree_index = int(line.split('#')[1].strip())
            elif not line or line[0] not in ["v", "e"]:
                # Check for the 'where' code output line
                if line.startswith('where:'):
                    where_str = line[8:-1]
                    where_arr = where_str.split(', ')
                    where_arr = [int(val) for val in where_arr]

                    # Store the 'where' code output in the dictionary
                    where_code_output[tree_index] = where_arr

                # Remove the line from the list of lines
                lines.remove(line)

        # Join the modified lines back into a string for the frequent subgraph
        frequent_subgraphs[i] = '\n'.join(lines)

    # Return the modified frequent subgraphs and the 'where' code output dictionary
    return frequent_subgraphs, where_code_output
