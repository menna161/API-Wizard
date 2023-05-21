from helpers.parse_file import parse_file
from m4_maximal_frequent_subtrees.mine_frequent_subgraphs import mine_frequent_subgraphs


#this function obtains the list of maximal frequent subgraphs  after removing the meaningless patterns from it and removing any subgraphs
def get_code_templates():
  # get subgraphs from 'output.txt' using the parse_file function
  extracted_subgraphs = parse_file('output.txt')
  print('Patterns Extracted From Code Snippets using Gspan: ', len(extracted_subgraphs))

  # Remove meaningless patterns by filtering out subgraphs that don't contain any lines with '#' (no api names)
  extracted_subgraphs = [s for s in extracted_subgraphs if any(c for c in s.split("\n")[1:] if ("#" in c ) )] #removes meaningless patterns
  print('Patterns After Removing Meaningless Patterns from Gspan: ', len(extracted_subgraphs))
   
   # obtain maximal frequent subgraphs using the mine_frequent_subgraphs function
  extracted_subgraphs, where_code_output = mine_frequent_subgraphs(extracted_subgraphs)
  print('Patterns After Removing Subgraphs: ',len(extracted_subgraphs))   

  return extracted_subgraphs, where_code_output