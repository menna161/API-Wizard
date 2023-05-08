"""# Fill Placeholders"""
from files_to_arrays import *
from pattern_to_code import *


def parallel_bfs_placeholder(lg_v, sm_v, adj_list_lg, adj_list_sm, start_node):
    # Initialize two empty sets 'visited_lg' and 'visited_sm', and two empty queues 'queue_lg' and 'queue_sm'.
    visited_lg = set()
    visited_sm = set()

    # Add the starting node to both 'visited_lg' and 'visited_sm', and to 'queue_lg' with an empty string,
    # and to 'queue_sm' with a node 0 and an empty string.
    queue_lg = deque([(start_node, '')])
    queue_sm = deque([(0, '')])
    visited_lg.add(start_node)
    visited_sm.add(0)

    tmp_score = {}
    placeholder_n = 0

    while len(queue_lg) > 0:
        isPlaceholder = False
        # print('before pop queue_lg',queue_lg)
        # print('before pop queue_sm',queue_sm)
        # Check if 'queue_lg' is empty, and if so, return False. Otherwise, dequeue the first node from both 'queue_lg' and 'queue_sm'.

        # print('queue_sm', queue_sm)
        if (len(queue_sm) == 0):
            queue_sm.clear()
            queue_sm = deque([(0, '')])
            return tmp_score

        node1 = queue_lg[0]
        node2 = queue_sm[0]
        # print('node1',lg_v[node1[0]])
        # print('node2',sm_v[node2[0]])
        # print('adj_list_lg', adj_list_lg)
        # print('adj_list_sm', adj_list_sm)

        # print('lg_name',lg_v[node1[0]])
        # print('sm_name',sm_v[node2[0]])
        # node1 = queue_lg.popleft()
        # node2 = queue_sm.popleft()

        # Check if the names of the nodes in 'lg_v' and 'sm_v' dictionaries are the same, and if not, return False.
        # if(lg_v[node1[0]] != sm_v[node2[0]]): return False;

        if ('PLACEHOLDER' in sm_v[node2[0]] or '(.*)' in sm_v[node2[0]]):
            isPlaceholder = True
            sm_v[node2[0]] = sm_v[node2[0]].replace('PLACEHOLDER', '(.*)')
            tmp_score['placeholder'+str(placeholder_n)] = {}

        match = re.findall(sm_v[node2[0]], lg_v[node1[0]])

        if (not match):
            # print('not equal will pop from large only 1')
            node1 = queue_lg.popleft()
            # print('if queue_lg',queue_lg)
            # print('if queue_sm',queue_sm)
            continue

        # check if the edges name are the same
        # elif(node1[1] != node2[1]):
        #     # print('not equal will pop from large only 2')
        #     node1 = queue_lg.popleft()
        #     # print('else queue_lg',queue_lg)
        #     # print('else queue_sm',queue_sm)
        #     continue;

        else:

            # print('matchhhh', match[0])
            # print('isPlaceholder', isPlaceholder)
            if isPlaceholder:
                # print('added in temp_score ', placeholder_n, match[0])
                tmp_score['placeholder'+str(placeholder_n)][match[0]] = 1
                placeholder_n = placeholder_n+1
            node1 = queue_lg.popleft()
            node2 = queue_sm.popleft()
            # print('after pop queue_lg',queue_lg)
            # print('after pop queue_sm',queue_sm)

        # Extract the node numbers from node1 and node2
        node1 = node1[0]
        node2 = node2[0]

        # For each neighbor of node1 in the larger graph, add it to 'queue_lg' and 'visited_lg' if it has not already been visited.
        # print('adj_list_lg[node1]', adj_list_lg[node1])
        # print('adj_list_sm[node2]', adj_list_sm[node2])

        for neighbor in adj_list_lg[node1]:
            if neighbor[0] not in visited_lg:
                visited_lg.add(neighbor[0])
                queue_lg.append((neighbor[0], neighbor[2]))

        # For each neighbor of node2 in the smaller graph, add it to 'queue_sm' and 'visited_sm' if it has not already been visited.
        for neighbor in adj_list_sm[node2]:
            if neighbor[0] not in visited_sm:
                visited_sm.add(neighbor[0])
                queue_sm.append((neighbor[0], neighbor[2]))

    # Return True if the while loop is exited, which indicates that all nodes in the smaller graph have been visited and matched to nodes in the larger graph.
    # so indicates the sammler graph is a subgraph
    # print('queue_sm ', queue_sm)
    if (len(queue_sm) != 0):
        return None
    return tmp_score


def placeholder_bfs_helper(lgGraph, smGraph, new_template):
    lg_v = {}
    sm_v = {}
    # score={}

    lg_v, sm_v, lg_edges, sm_edges = representing_trees(lgGraph, smGraph)

    # search for the first occurence of the node
    search_string = sm_v[0]
    found_search = False
    foundV_key = 0
    # print("search_string",search_string)

    if (new_template):
        i = 0
        for key, value in sm_v.items():
            if 'PLACEHOLDER' in value:
                # print('value' , value)
                score['placeholder'+str(i)] = {}
                i = i+1
        new_template = False

    # Looping through all nodes in the larger graph and searching for a matching node
    # to check the possibility of finding a subgraph
    # print('lg_v', lg_v)
    # print('sm_v', sm_v)
    # print('lg_edges', lg_edges)
    # print('sm_edges', sm_edges)

    for key, value in lg_v.items():
        # print("value" , value)
        # print("search_string" , search_string)

        matches = re.findall(re.escape(value), search_string)
        if matches:
            for match in matches:

                foundV_key = key
                # print('foundV_key', foundV_key)
                tmp_score = parallel_bfs_placeholder(
                    lg_v, sm_v, lg_edges, sm_edges, foundV_key)

                if (tmp_score is not None):
                    found_search = True
                    # print('tmp_score ', tmp_score)
                    for key, values in tmp_score.items():
                        for sub_key, sub_value in values.items():
                            if key in score and sub_key in score[key]:
                                score[key][sub_key] = score[key][sub_key] + \
                                    1 if sub_key in tmp_score[key] else score[key][sub_key]
                            else:
                                score[key][sub_key] = 1

    # If no matching node was found or the graphs are not subgraphs, return
    # if (not found_search) :
    if (found_search):

        # print(f'The Two graphs are NOT subgraph')
        return score
    else:
        # print(f'found a subgraph')
        print('##############did not find the pattern in the big tree')
        return None


def get_var_names(snippets_scores, snippet_num):
    vars = []
    placeholder_dict = snippets_scores.get(snippet_num, {})
    # print(f"Subkeys of values in {snippet_num}:")
    for placeholder in placeholder_dict.values():
        for sub_key in placeholder.keys():
            vars.append(sub_key)
    return vars

# def calc_scores(where_code_output, code_output_ast):


def calc_scores(where_code_output, extracted_subgraphs):
    snippets_scores = {}

    # ast_to_gspan("code_templates.txt" , code_output_ast ,True)
    # templates_gspan_snippets= parse_file('code_templates.txt')
    # templates_gspan_snippets = templates_gspan_snippets[:-1]
    templates_gspan_snippets = extracted_subgraphs
    print('templates_gspan_snippets', templates_gspan_snippets)
    input_with_vars_gspan_snippets = parse_file('input_with_vars.txt')
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
                template_score = placeholder_bfs_helper(
                    input_with_vars_gspan_snippets[code_snippet], template, new_template)
                new_template = False
                # print('template_score ', template_score)
            # print('templateee', template)
            if (template_score is not None):
                # print('template_score ', template_score)
                placeholder_fillings = {}
                for key in template_score:

                    placeholder_score = template_score[key]
                    # try:
                    max_inner_key = max(placeholder_score,
                                        key=placeholder_score.get)
                    max_value = placeholder_score[max_inner_key]
                    placeholder_fillings[key] = {}
                    placeholder_fillings[key][max_inner_key] = max_value
                    # print('placeholder_fillings  ', placeholder_fillings)
                    # except:
                    #   placeholder_fillings[key] ={}
                    #   placeholder_fillings[key]['PLACEHOLDER'] = 0
                    # print('###################before bfs_helper template number ', index)
                    # print('###################before bfs_helper code_snippet from input', code_snippet)
                    # print('placeholder_score', placeholder_score)
                    # pass

                snippets_scores[index] = placeholder_fillings

    print('snippets_scores', snippets_scores)

    code_out = fill_placeholder(
        snippets_scores, templates_gspan_snippets, where_code_output)
    print("###########333333")
    for t in templates_gspan_snippets:
        print(t)
    return code_out


def fill_placeholder(snippets_scores, templates_gspan_snippets, where_code_output):
    for index, template in enumerate(templates_gspan_snippets):
        #   # i=0
        # print(template)
        vars = get_var_names(snippets_scores, index)
        # print(vars)

        for var in vars:
            template = template.replace("PLACEHOLDER", var, 1)
            # print('template after edit', template)

        templates_gspan_snippets[index] = template
    # print('templates_gspan_snippets', templates_gspan_snippets)
    # print('before code output ', code_output)
    # print(' where code output in fill_placeholder', where_code_output)

    code_out, ast_out = parse_ast_helper(
        templates_gspan_snippets, where_code_output)

    # print('after code output ', code_output)
    # print('after where code output ', where_code_output)
    # print('complete out', code_out)
    return code_out


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
