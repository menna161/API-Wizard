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
    api_name = 'MinMaxScaler'
    ex = read_dir(api_name)
    input_count, trees = snippets_to_ast(ex)
    
    ast_to_gspan('input.txt', trees)
    ast_to_gspan('input_with_vars.txt', trees, True)
    common_patterns()

    extracted_subgraphs, where_code_output =  get_code_templates()
    extracted_subgraphs = add_placeholders(extracted_subgraphs)
    print('Generated Code Templats Successfully')
    
    code_output = calc_scores(where_code_output, extracted_subgraphs)


    print('################################ Output #################################')
    unique_list = sort_lines(code_output)
    unique_list = remove_repeated(unique_list)
    unique_list = sorted(unique_list, key=custom_key)
    unique_list = remove_placeholders(unique_list)
    joined_lines = ''.join(unique_list)
    print(joined_lines)

    
    print('################################ Evaluation ################################')
    
    repr = calc_representative(where_code_output, input_count)
    print('representativeness:   ', repr)

    consiceness = calc_consiceness(unique_list)
    print('conciseness:   ', consiceness)


if __name__ == "__main__":
    main()
