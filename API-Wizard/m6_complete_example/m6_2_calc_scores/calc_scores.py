from helpers.parse_file import parse_file
from ..m6_1_match_placeholders.placeholder_bfs_helper import placeholder_bfs_helper
from ..m6_3_generate_complete_code.fill_placeholder import fill_placeholder

# def calc_scores(where_code_output, code_output_ast):
def calc_scores(where_code_output, extracted_subgraphs):
  snippets_scores= {}
  vertices = {}

  # ast_to_gspan("code_templates.txt" , code_output_ast ,True)
  # templates_gspan_snippets= parse_file('code_templates.txt')
  # templates_gspan_snippets = templates_gspan_snippets[:-1]
  templates_gspan_snippets = extracted_subgraphs
  # print('templates_gspan_snippets', templates_gspan_snippets)
  input_with_vars_gspan_snippets= parse_file('input_with_vars.txt')
  input_with_vars_gspan_snippets = input_with_vars_gspan_snippets[:-1]
  # print('templates_gspan_snippets', json.dumps(templates_gspan_snippets, indent=2))
  # print('input_with_vars_gspan_snippets', json.dumps(input_with_vars_gspan_snippets, indent=2))

  # print('input_with_vars_gspan_snippets', input_with_vars_gspan_snippets)
  # print('templates_gspan_snippets', templates_gspan_snippets)


  for index, template in enumerate(templates_gspan_snippets):
    if 'PLACEHOLDER' in template:
      new_template = True
      
      for code_snippet in where_code_output[index]:
        # print('###################before bfs_helper template number ', index)
        # print('###################before bfs_helper code_snippet from input', code_snippet)
        # print('indexxx', code_snippet)
        # print('template_score template score index ', index, 'code_snippet: ', code_snippet)
        template_score, vertex_numbers= placeholder_bfs_helper(input_with_vars_gspan_snippets[code_snippet], template ,new_template)
        # print('template_score ', template_score)
        new_template= False
        # print("vertex_numbers",vertex_numbers)
      # print('templateee', template)
      if(template_score is not None):
        # print('template_score ', template_score)
        placeholder_fillings = {}
        for key in template_score:
          
            placeholder_score = template_score[key]
            # try:
            max_inner_key = max(placeholder_score, key=placeholder_score.get)
            max_value = placeholder_score[max_inner_key]
            placeholder_fillings[key] ={}
            placeholder_fillings[key][max_inner_key]= max_value
              # print('placeholder_fillings  ', placeholder_fillings)
            # except:
            #   placeholder_fillings[key] ={}
            #   placeholder_fillings[key]['PLACEHOLDER'] = 0
              # print('###################before bfs_helper template number ', index)
              # print('###################before bfs_helper code_snippet from input', code_snippet)
              # print('placeholder_score', placeholder_score)
              # pass

        snippets_scores[index]= placeholder_fillings
        vertices[index]= vertex_numbers
      
  
  code_out = fill_placeholder(snippets_scores, templates_gspan_snippets, where_code_output ,vertices)
  print("Calculated Scores for Placeholders Successfully\n")

  return code_out

