from ..m6_2_calc_scores.get_var_names import get_var_names
from .parse_ast_helper import parse_ast_helper

def fill_placeholder(snippets_scores, templates_gspan_snippets, where_code_output,vertices):
  for index, values in vertices.items():
  #   # i=0
    # print(template)
    vars = get_var_names(snippets_scores, index)

    for i, node_num in enumerate(values):
      lines = templates_gspan_snippets[index].split('\n')
      for j, line in enumerate(lines):
        if line and line.startswith("v "+str(node_num)) and "PLACEHOLDER" in line:
          # print(line)
          # print('#####vars[i]',vars[i])
          line = line.replace("PLACEHOLDER", vars[i], 1)
          # print('line after edited',line)
          lines[j] = line  # update the line in the list
          break
      templates_gspan_snippets[index] = "\n".join(lines)  # join the updated lines and assign back to the original string




  
  code_out, ast_out = parse_ast_helper(templates_gspan_snippets, where_code_output)
  

  return code_out