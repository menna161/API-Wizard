from helpers.parse_file import parse_file
from m4_maximal_frequent_subtrees.mine_frequent_subgraphs import mine_frequent_subgraphs

def get_code_templates():
  extracted_subgraphs = parse_file('output.txt')
  print('Patterns Extracted From Code Snippets using Gspan: ', len(extracted_subgraphs))
  extracted_subgraphs = [s for s in extracted_subgraphs if any(c for c in s.split("\n")[1:] if ("#" in c ) )] #removes meaningless patterns
  print('Patterns After Removing Meaningless Patterns from Gspan: ', len(extracted_subgraphs))
  

  extracted_subgraphs, where_code_output = mine_frequent_subgraphs(extracted_subgraphs)
  print('Patterns After Removing Subgraphs: ',len(extracted_subgraphs))

      

  return extracted_subgraphs, where_code_output