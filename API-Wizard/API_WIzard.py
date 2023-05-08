# import libraries
import json
import os
import ast
import astor
import re
import pandas
from os import fsdecode
from collections import deque
import subprocess
import warnings

# import functions
from read_dir import *
from snippets_to_ast import *
from ast_to_gspan import *
from find_common_patterns import *
from files_to_arrays import *
from bfs_subgraph import *
from representing_trees import *
from maximal_frequent_subgraphs import *
from code_templates import *
from pattern_to_code import *
from fill_placeholders import *
from evaluation import *


"""#Driver Code"""


def main():

    api_name = 'MinMaxScaler'
    ex = read_dir(api_name)
    input_count, trees = snippets_to_ast(ex)

    ast_to_gspan('input.txt', trees)
    ast_to_gspan('input_with_vars.txt', trees, True)
    common_patterns(trees)

    extracted_subgraphs, where_code_output = get_code_templates()
    print('extracted_subgraphssssss after removing subgraphs',
          len(extracted_subgraphs))
    for f in extracted_subgraphs:
        print(f+'\n')

    extracted_subgraphs = add_placeholders(extracted_subgraphs)

    print('afteer adding placeholders ')
    for f in extracted_subgraphs:
        print(f+'\n')

    # print('extracted_subgraphs ', extracted_subgraphs)
    # code_output, code_output_ast = parse_ast_helper(extracted_subgraphs, where_code_output)
    # print('extracted_subgraphssssss', len(code_output_ast))
    # print('codee outt [12] ', ast.dump(code_output_ast[12]))

    # for index,out in enumerate(code_output):
    # #   # print(where_code_output[index])
    #   print('code_out_ast', ast.dump(code_output_ast[index]))
    #   print(out)

    # joined_lines = ''.join(code_output)
    # print(joined_lines)

    code_output = calc_scores(where_code_output, extracted_subgraphs)

    print('code_output ', code_output)
    print('whereee', where_code_output)

    print('################################ Output #################################')
    joined_lines = ''.join(set(code_output))
    print(joined_lines)
    # print("---------------------")
    # for c in code_output:
    #   print(c)

    # print("where_code_output", where_code_output)
    # print("where_code_output len", len(where_code_output))
    # print("code_output len", len(code_output))

    print('################################ Evaluation ################################')

    repr = calc_representative(where_code_output, input_count)
    print('representativeness:   ', repr)

    consiceness = calc_consiceness(code_output)
    print('conciseness:   ', consiceness)


ex = []  # filtered code examples in the dataset
trees = []  # ast trees of the filtered code examples
input_count = 0
# dumps = []
extracted_subgraphs = []  # Gspan format of all output patterns
# frequent_subgraphs = [] # final frequent subgraphs after processing (removing subgraphs and meaningless trees) gspan format
where_code_output = []  # array of the source of each pattern# lg_v = {}
# sm_v = {}

code_output = []  # pattern output code with placeholder
code_output_ast = []  # pattern output ast tree with placeholder

score = {}  # to store trees scores

if __name__ == "__main__":
    main()
