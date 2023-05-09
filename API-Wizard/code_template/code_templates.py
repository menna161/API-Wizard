"""#Code Templates"""
from files_to_arrays import *
from maximal_frequent_subgraphs import *


def get_code_templates():
    where_code_output = []
    extracted_subgraphs = parse_file('output.txt')
    print('patterns extracted from gspan: ', len(extracted_subgraphs))
    extracted_subgraphs = [s for s in extracted_subgraphs if any(
        c for c in s.split("\n")[1:] if ("#" in c))]  # removes meaningless patterns
    print('patterns after removing meaningless patterns from gspan: ',
          len(extracted_subgraphs))
    extracted_subgraphs, where_code_output = mine_frequent_subgraphs(
        extracted_subgraphs)
    print('patterns after removing subgraphs: ', len(extracted_subgraphs))
    print('extracted_subgraphs after mine_frequent_subgraphs: ', extracted_subgraphs)
    extracted_subgraphs, where_code_output = mine_frequent_subgraphs(
        extracted_subgraphs)
    print('extracted_subgraphs after mine_frequent_subgraphs TWICEEEE: ',
          extracted_subgraphs)

    extracted_subgraphs, where_code_output = mine_frequent_subgraphs_helper(
        extracted_subgraphs)

    return extracted_subgraphs, where_code_output
