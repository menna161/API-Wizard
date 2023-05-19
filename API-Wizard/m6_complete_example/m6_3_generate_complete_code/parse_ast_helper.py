import ast
from .parse_ast import parse_ast
import astor

def parse_ast_helper(frequent_subgraphs, where_code_output):

  code_output = []
  code_output_ast = []
  for index,tree in enumerate(frequent_subgraphs):
    lines = tree.split('\n')
    nodes = []
    edges = []
    

    # Iterate over the lines and parse the nodes and edges
    for line in lines:
        if line.startswith('v '):
            # print('line   ', line)
            _, i, node = line.split(' ')
          
            nodes.append(node)
        elif line.startswith('e '):
            _, source, target, edge_type = line.split(' ')
            edges.append((int(source), int(target), edge_type))
    
    root = parse_ast(nodes,edges)
    
    # print('indexxxx', index)
    # print('where_code_output in parse ast ',where_code_output)
    try:
      code_output.append(astor.to_source(root))
      code_output_ast.append(root)
      # print(astor.to_source(root))
    except:
      print('failed to convert ast to code: ', ast.dump(root))
      # print(index)
      del where_code_output[index]
      pass
  return code_output, code_output_ast