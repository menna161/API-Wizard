# import libraries
import json
import os
import ast
import astor
import pandas
from os import fsdecode
import subprocess


# import functions
from m1_filtered_code_snippets.read_dir import read_dir
from m2_constructing_asts.snippets_to_ast import snippets_to_ast
from m3_gspan_pattern_mining.ast_to_gspan import ast_to_gspan
from m3_gspan_pattern_mining.common_patterns import common_patterns
from m5_generate_code_template.get_code_templates import get_code_templates
from m5_generate_code_template.add_placeholders import add_placeholders
from m6_complete_example.m6_2_calc_scores.calc_scores import calc_scores
from helpers.sort_lines import sort_lines
from helpers.remove_repeated import remove_repeated
from helpers.custom_key import custom_key
from helpers.remove_placeholders import remove_placeholders
from evaluation.calc_representative import calc_representative
from evaluation.calc_consiceness import calc_consiceness 

#Driver Code

def main():
    #pass the api name you want an example for 
    # api_name = 'tf.pad'
    api_name = input('')
    #check the path of the dataset is correct inside read_dir

    # m1 get the filtered code snippets
    ex = read_dir(api_name)
    # m2 for each snippet construct an ast tree
    input_count, trees = snippets_to_ast(ex)
    
    # m3 convert ast represenation to gspan 
    #version without var names (used to find common patterns)
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_file_path, 'input.txt')
    input_path = input_path.replace("\\", "/")
    print('updated_input_path', input_path)
    ast_to_gspan(input_path, trees)
    #version with var names (used to later to obtain placeholder values)
    input_with_vars_path = os.path.join(current_file_path, 'input_with_vars.txt')
    input_with_vars_path = input_with_vars_path.replace("\\", "/")
    print('updated_input_with_vars', input_with_vars_path)
    ast_to_gspan(input_with_vars_path, trees, True)
    #find common patterns in input.txt
    common_patterns()

    #m4 and m5 obtain maximal frequent subtrees and form a code template
    extracted_subgraphs, where_code_output =  get_code_templates()
    extracted_subgraphs = add_placeholders(extracted_subgraphs)
    print('Generated Code Templats Successfully')
    
    #m6 generate a complete code example by replacing placeholders with var and param names with max score
    code_output = calc_scores(where_code_output, extracted_subgraphs)

    print('Output')
    unique_list = sort_lines(code_output)
    unique_list = remove_repeated(unique_list)
    unique_list = sorted(unique_list, key=custom_key)
    unique_list = remove_placeholders(unique_list)
    joined_lines = ''.join(unique_list)
    print(joined_lines)

    print('Evaluation')
    
    repr = calc_representative(where_code_output, input_count)
    print('representativeness:   ', repr)

    consiceness = calc_consiceness(unique_list)
    print('conciseness:   ', consiceness)


if __name__ == "__main__":
    main()
