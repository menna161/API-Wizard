from helpers.parse_file import parse_file
from ..m6_1_match_placeholders.placeholder_bfs_helper import placeholder_bfs_helper
from ..m6_3_generate_complete_code.fill_placeholder import fill_placeholder

#this function matches each code template  placeholders with the corresponding variable names from the input example by using BFS
#iT keeps a count of the number of times each placeholder was matched and stores it in a dictionary
def calc_scores(where_code_output, extracted_subgraphs):
  snippets_scores = {}  # Stores the scores for each snippet
  vertices = {}  # Stores the vertex numbers for each snippet
  templates_gspan_snippets = extracted_subgraphs  # List of extracted subgraphs
  input_with_vars_gspan_snippets = parse_file('input_with_vars.txt')  # Parse input file with variable names
  input_with_vars_gspan_snippets = input_with_vars_gspan_snippets[:-1]  # Remove last element from input

# Iterate over each template in the extracted subgraphs
  for index, template in enumerate(templates_gspan_snippets):
    if 'PLACEHOLDER' in template:
      # Indicates if the current template is a new template or a continuation
      new_template = True
      
      # Iterate over each code snippet associated with the template
      for code_snippet in where_code_output[index]:
        # Call the placeholder_bfs_helper function to calculate the score and obtain vertex numbers
        template_score, vertex_numbers= placeholder_bfs_helper(input_with_vars_gspan_snippets[code_snippet], template ,new_template)
        new_template= False

      if(template_score is not None):
        placeholder_fillings = {}
         # Iterate over the keys in the template_score dictionary
        for key in template_score:
          
            placeholder_score = template_score[key]
             # Find the maximum value and corresponding key in the placeholder_score dictionary
            max_inner_key = max(placeholder_score, key=placeholder_score.get)
            max_value = placeholder_score[max_inner_key]
            placeholder_fillings[key] ={}
            # Store the maximum value and key in the placeholder_fillings dictionary
            placeholder_fillings[key][max_inner_key]= max_value

        # Store the placeholder scores for the snippet
        snippets_scores[index]= placeholder_fillings
        vertices[index]= vertex_numbers
      
  
  code_out = fill_placeholder(snippets_scores, templates_gspan_snippets, where_code_output ,vertices)
  print("Calculated Scores for Placeholders Successfully\n")

  return code_out

