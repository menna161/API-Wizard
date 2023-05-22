import ast
from .parse_ast import parse_ast
import astor


#helper function that converts trees in gspan format to ast tree representation and to pyhton code
def parse_ast_helper(frequent_subgraphs, where_code_output):
    code_output = []  # Stores the converted code
    code_output_ast = []  # Stores the AST (Abstract Syntax Tree)
    
    # Iterate over each index and tree in the frequent_subgraphs
    for index, tree in enumerate(frequent_subgraphs):
        lines = tree.split('\n')  # Split the tree into lines
        nodes = []  # Stores the nodes
        edges = []  # Stores the edges

        # Iterate over the lines and parse the nodes and edges
        for line in lines:
            if line.startswith('v '):
                _, i, node = line.split(' ')
                nodes.append(node)  # Append the node to the nodes list
            elif line.startswith('e '):
                _, source, target, edge_type = line.split(' ')
                edges.append((int(source), int(target), edge_type))  # Append the edge to the edges list

        root = parse_ast(nodes, edges)  # Call the parse_ast function to create the AST root node
        
        try:
            code_output.append(astor.to_source(root))  # Convert the AST to source code and append to code_output
            code_output_ast.append(root)  # Append the AST root node to code_output_ast
        except:
            print('failed to convert ast to code: ', ast.dump(root))
            del where_code_output[index]  # Remove the corresponding entry from where_code_output
            pass

    return code_output, code_output_ast
