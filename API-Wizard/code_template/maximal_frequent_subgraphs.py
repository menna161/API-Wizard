"""#Maximal Freqent Subgraphs algorithm"""


def mine_frequent_subgraphs_helper(frequent_subgraphs):
    where_code_output = []
    # print('helper', frequent_subgraphs)

    for i in range(len(frequent_subgraphs)):
        lines = frequent_subgraphs[i].split('\n')
        for line in lines.copy():
            if not line or line[0] not in ["v", "e"]:
                if line.startswith('where:'):
                    where_str = line[8:-1]
                    where_arr = where_str.split(', ')
                    where_arr = [int(val) for val in where_arr]
                    # print(where_arr)
                    where_code_output.append(where_arr)
                    # print('where', where_code_output)
                lines.remove(line)
        frequent_subgraphs[i] = '\n'.join(lines)
    return frequent_subgraphs, where_code_output


def mine_frequent_subgraphs(frequent_subgraphs):
    where_code_output = []
    lg_v = {}
    sm_v = {}

    frequent_subgraphs.sort(key=lambda x: len(x))

    sml_pointer = 0
    lg_pointer = len(frequent_subgraphs) - 1

    while sml_pointer < len(frequent_subgraphs):
        sml_pointer_temp = sml_pointer
        while sml_pointer < lg_pointer:

            lg_v, sm_v, lg_edges, sm_edges = representing_trees(
                frequent_subgraphs[lg_pointer], frequent_subgraphs[sml_pointer])

            if parallel_bfs_supgraphs_helper(lg_v, sm_v, lg_edges, sm_edges):

                frequent_subgraphs.pop(sml_pointer)
                lg_pointer = len(frequent_subgraphs) - 1

            else:
                # sml_pointer += 1
                lg_pointer -= 1
        sml_pointer = sml_pointer_temp+1
        lg_pointer = len(frequent_subgraphs) - 1

    # frequent_subgraphs, where_code_output = mine_frequent_subgraphs_helper(frequent_subgraphs)

    return frequent_subgraphs, where_code_output
