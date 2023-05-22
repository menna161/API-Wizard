from ..m6_2_calc_scores.get_var_names import get_var_names
from .parse_ast_helper import parse_ast_helper

#this function replaces all the placeholders with their corressponding var \ parameter names
#based on the correct vertex number
def fill_placeholder(snippets_scores, templates_gspan_snippets, where_code_output, vertices):
    # Iterate over each index and its corresponding vertex values in the vertices dictionary
    for index, values in vertices.items():
        vars = get_var_names(snippets_scores, index)  # Get the variable names from snippets_scores using the index

        # Iterate over each value (node number) in the values list
        for i, node_num in enumerate(values):
            lines = templates_gspan_snippets[index].split('\n')  # Split the template into lines

            # Iterate over each line in the lines list
            for j, line in enumerate(lines):
                if line and line.startswith("v " + str(node_num)) and "PLACEHOLDER" in line:
                    # If the line starts with "v <node_num>" and contains "PLACEHOLDER", replace "PLACEHOLDER" with the variable
                    line = line.replace("PLACEHOLDER", vars[i], 1)
                    lines[j] = line  # Update the line in the list
                    break  # Break the loop after finding and updating the line

            templates_gspan_snippets[index] = "\n".join(lines)  # Join the updated lines and assign back to the original string

    code_out, ast_out = parse_ast_helper(templates_gspan_snippets, where_code_output)  # Call parse_ast_helper

    return code_out
