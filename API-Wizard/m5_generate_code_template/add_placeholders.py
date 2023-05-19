def add_placeholders(extracted_subgraphs):
  for i_tree, tree in enumerate(extracted_subgraphs):

    lines = tree.split('\n')    

    # Iterate over the lines and parse the nodes and edges
    for index, line in enumerate(lines):
        if line.startswith('v '):
            # print('line   ', line)
            _, i, node = line.split(' ')
            if node in ('Name', 'arg'):
                node = str(node)+"#id=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line
            if node in ('Attribute'):
                node = str(node)+"#attr=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line
            if node in ('Constant'):
                node = str(node)+"#value=PLACEHOLDER"
                line = 'v '+str(i)+' '+node
                lines[index] = line

    
    extracted_subgraphs[i_tree] = "\n".join(lines)
  return extracted_subgraphs