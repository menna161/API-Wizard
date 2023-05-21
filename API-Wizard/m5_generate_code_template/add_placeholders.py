
#this function searches for the nodes that would usually contain variable/parameter names 
#initially defines them as "placeholders" to generate a code template 
#retruns the extrcted trees with placeholders that represents variable/parameter names 
def add_placeholders(extracted_subgraphs):
# Iterate over the extracted subgraphs
  for i_tree, tree in enumerate(extracted_subgraphs):

    lines = tree.split('\n')    

    # Iterate over the lines and parse the nodes and edges
    for index, line in enumerate(lines):
        if line.startswith('v '):
            _, i, node = line.split(' ')
            # Check if the node is 'Name' or 'arg' and add a placeholder 
            if node in ('Name', 'arg'):
                node = str(node)+"#id=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line
             # Check if the node is 'Attribute' and add a placeholder 
            if node in ('Attribute'):
                node = str(node)+"#attr=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line
             # Check if the node is 'Constant' and add a placeholder 
            if node in ('Constant'):
                node = str(node)+"#value=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line

     # Update the modified lines in the extracted subgraph
    extracted_subgraphs[i_tree] = "\n".join(lines)
  return extracted_subgraphs