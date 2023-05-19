from flask import Flask, jsonify, request
import json
import os
import ast
import astor
import re
import warnings
import pandas
from os import fsdecode
from collections import deque
import subprocess
import re

# ex = []
trees = []
dumps = []
extracted_subgraphs2 = []
fg = []
lg_v = {}
sm_v = {}
where_code_output = []
code_output = []


def read_dir(api):
    pdir_path = '/Users/nehalfooda/Downloads/Thesis/API/'
    # The API name from the user
    api_file_name = 'MinMaxScaler'
    dir_path = pdir_path + api

    ex = []

    for file_name in os.listdir(dir_path):
        if file_name.endswith('.py'):
            with open(os.path.join(dir_path, file_name), 'r') as file:
                text = file.read()
                ex.append(text)
    return ex
    # print(ex)
    # print(len(ex))
    # print("read dir")


def snippets_to_ast(ex):
    for e in ex:
        trees.append(ast.parse(e))

    for tree in trees:
        dumps.append(ast.dump(tree))

    # len_ex = len(dumps)
    # print(dumps)
    # print("snippets_to_ast")


def ast_to_gspan():
    file = open("input.txt", "w")
    i = 0
    for snippet_tree in trees:
        v_write = []
        e_write = []
        v_n = 0
        parent_n = -1
        file.write(f't # {i}\n')
        file.write(f'v 0 Module\n')
        i += 1

        for node in ast.walk(snippet_tree):
            n = str(node).split()[0][6:]
            # print('node',node,list(ast.iter_child_nodes(node)))
            parent_n += 1
            children = []
            e_n = 0
            fields = list(ast.iter_fields(node))
            for index, x in enumerate(ast.iter_child_nodes(node)):
                child = type(x).__name__
                # print('child',index, child)
                try:
                    # check if the child is ImportFrom to add Module
                    if (child == "ImportFrom"):
                        child = str(child) + "#module=" + x.module

                    # check if the node is alias with parent Import
                    elif (type(node).__name__ in ('Import', 'ImportFrom') and child == 'alias'):
                        child = str(child) + "#name="+x.name
                        if (x.asname is not None):
                            child = str(child) + "#asname="+x.asname
                    elif (index < len(fields) and fields[index][0] == 'func'):
                        for item, val in ast.iter_fields(x):
                            if (item in ("name", "id", "attr")):
                                child = str(child) + "#"+item+"="+val
                    elif (child in ('FunctionDef', 'AsyncFunctionDef', 'ClassDef')):
                        child = str(child) + "#name=" + x.name
                    elif (child == "Constant"):
                        child = str(child) + "#value=" + \
                            str(x.value).replace(" ", "")
                        if x.kind is not None:
                            child = child + "#kind=" + str(x.kind)
                    elif (child == "FormattedValue"):
                        child = str(child) + "#conversion=" + str(x.conversion)
                    elif (child == "AnnAssign"):
                        child = str(child) + "#simple=" + str(x.simple)
                    elif (child == "ExceptHandler"):
                        if (x.name is not None):
                            child = str(child) + "#name=" + str(x.name)
                    elif (child in ("Global", "Nonlocal")):
                        print('gloabl or nonlocal', type(x.names))
                        placeholders_count = len(x.names)
                        print('count', placeholders_count)
                        child = str(child) + "#names_count=" + \
                            str(placeholders_count)
                    elif (child == "keyword"):
                        if (x.arg is not None):
                            child = str(child) + "#arg=" + str(x.arg)
                except:
                    pass

                v_n += 1
                # print('v '+str(v_n)+' '+str(child)+'\n')
                # file_write.append('v '+str(v_n)+' '+str(child)+'\n')
                v_write.append('v '+str(v_n)+' '+str(child)+'\n')
                children.append([child, v_n])

            edges_list = list(ast.iter_fields(node))
            # print('fields', edges_list)

            for edge in list(ast.iter_fields(node)):
                # print('loop edges', edge[0], edge[1], type(edge[1]))
                if (not isinstance(edge[1], ast.AST) and not isinstance(edge[1], list)):
                    # print('not AST')
                    continue

                if len(children) > 0:
                    if isinstance(edge[1], list):
                        # should we put any list as keywords0 sice we already checked it is a list
                        if (len(edge[1]) == 1):
                            try:
                                if (str(edge[0]) == 'keywords'):
                                    edge[0] = 'keywords0'
                                # print('e1 '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                                # file_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                                e_write.append(
                                    'e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                            except:
                                pass
                            e_n += 1
                        else:
                            edge_name_n = 0
                            for node in edge[1]:
                                # print('e2 '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0]+str(edge_name_n))+'\n')
                                # file_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0]+str(edge_name_n))+'\n')
                                e_write.append(
                                    'e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0]+str(edge_name_n))+'\n')
                                e_n += 1
                                edge_name_n += 1
                    else:
                        try:
                            if (str(edge[0]) == 'keywords'):
                                edge[0] = 'keywords0'
                            # print('e3 '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                            # file_write.append('e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                            e_write.append(
                                'e '+str(parent_n)+' '+str(children[e_n][1])+' '+str(edge[0])+'\n')
                        except:
                            pass
                        e_n += 1

        # file_write.sort()
        # sort the array based on the number after v in each string
        v_write = sorted(v_write, key=lambda x: int(
            re.search(r'v (\d+)', x).group(1)))

        e_write = sorted(e_write, key=lambda x: int(
            re.search(r'e (\d+)', x).group(1)))

        for y in v_write:
            file.write(y)

        for y in e_write:
            file.write(y)

    # for y in reversed(file_write):
    #   file.write(y)

    file.write("t # -1\n")
    file.close()
    # print("ast_to_gspan")


def common_patterns():
    warnings.filterwarnings('ignore')
    len_ex = len(dumps)
    minsupport = int(len_ex/2)
    #  -w True
    os.system(
        "python -m gspan_mining -s " + str(minsupport)+" -d True -w True ./input.txt > output.txt")

    # print("common_patterns")


def array_of_patterns():
    # Open the input file for reading
    with open('output.txt', 'r') as file:
        extracted_subgraphs = []
        current_string = ''
        # Loop over each line in the file
        for line in file:
            # Check if the line starts with 't'
            if line.startswith('t'):
                # If so, append the current string to the array (if it's not empty)
                if current_string:
                    extracted_subgraphs.append(current_string.strip())
                # Start a new current string
                current_string = line
            # Otherwise, append the line to the current string
            else:
                current_string += line

        # Append the last current string to the array (if it's not empty)
        if current_string:
            extracted_subgraphs.append(current_string.strip())

    # Remove the 'Support' line and dashes from each extracted string
    for i in range(len(extracted_subgraphs)):
        extracted_subgraphs[i] = '\n'.join([line for line in extracted_subgraphs[i].split(
            '\n') if not line.startswith(('Support', '-'))]).strip()

    # Remove Meaningless Patterns
    extracted_subgraphs = [s for s in extracted_subgraphs if any(
        c for c in s.split("\n")[1:] if "#" in c)]
    extracted_subgraphs2 = extracted_subgraphs
    # print(len(extracted_subgraphs2))
    # print(len(extracted_subgraphs))

    # print("array_of_patterns")
    return extracted_subgraphs


# Define a function named 'parallel_bfs' that takes in three arguments: two adjacency lists (adj_list_lg and adj_list_sm) and a starting node.
def parallel_bfs(adj_list_lg, adj_list_sm, start_node):
    # Initialize two empty sets 'visited_lg' and 'visited_sm', and two empty queues 'queue_lg' and 'queue_sm'.
    visited_lg = set()
    visited_sm = set()

    # Add the starting node to both 'visited_lg' and 'visited_sm', and to 'queue_lg' with an empty string,
    # and to 'queue_sm' with a node 0 and an empty string.
    queue_lg = deque([(start_node, '')])
    queue_sm = deque([(0, '')])
    visited_lg.add(start_node)
    visited_sm.add(0)

    while len(queue_sm) > 0:
        # print('before pop queue_lg',queue_lg)
        # print('before pop queue_sm',queue_sm)
        # Check if 'queue_lg' is empty, and if so, return False. Otherwise, dequeue the first node from both 'queue_lg' and 'queue_sm'.
        if (len(queue_lg) == 0):
            return False

        node1 = queue_lg[0]
        node2 = queue_sm[0]
        # print('lg_name',lg_v[node1[0]])
        # print('sm_name',sm_v[node2[0]])
        # node1 = queue_lg.popleft()
        # node2 = queue_sm.popleft()

        # Check if the names of the nodes in 'lg_v' and 'sm_v' dictionaries are the same, and if not, return False.
        # if(lg_v[node1[0]] != sm_v[node2[0]]): return False;
        if (lg_v[node1[0]] != sm_v[node2[0]]):
            # print('not equal will pop from large only 1')
            node1 = queue_lg.popleft()
            # print('if queue_lg',queue_lg)
            # print('if queue_sm',queue_sm)
            continue

        # check if the labels of the nodes are the same, and if not, return False.
        # if(node1[1] != node2[1]): return False;
        elif (node1[1] != node2[1]):
            # print('not equal will pop from large only 2')
            node1 = queue_lg.popleft()
            # print('else queue_lg',queue_lg)
            # print('else queue_sm',queue_sm)
            continue

        else:
            node1 = queue_lg.popleft()
            node2 = queue_sm.popleft()
            # print('after pop queue_lg',queue_lg)
            # print('after pop queue_sm',queue_sm)

        # Extract the node numbers from node1 and node2
        node1 = node1[0]
        node2 = node2[0]

        # For each neighbor of node1 in the larger graph, add it to 'queue_lg' and 'visited_lg' if it has not already been visited.
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
    return True

# str1 is the bigger graph


def representing_trees(lgGraph, smGraph):

    # Clearing the vertex dictionaries
    lg_v.clear()
    sm_v.clear()

    # Finding all lines that start with 'v' and 'e' in both graphs
    v_lines_lgGraph = re.findall(r"^v\s.*", lgGraph, re.MULTILINE)
    e_lines_lgGraph = re.findall(r"^e\s.*", lgGraph, re.MULTILINE)
    v_lines_smGraph = re.findall(r"^v\s.*", smGraph, re.MULTILINE)
    e_lines_smGraph = re.findall(r"^e\s.*", smGraph, re.MULTILINE)

    # This matches the vertices numbers and names in the larger graph and stores them in a dictionary
    for line in v_lines_lgGraph:
        num = line.split()
        lg_v[int(num[1])] = num[2]

    # This matches the vertices numbers and names in the smaller graph and stores them in a dictionary
    for line in v_lines_smGraph:
        num = line.split()
        sm_v[int(num[1])] = num[2]

    # Storing the last vertex number in each graph
    last_lgGraph = v_lines_lgGraph[-1].split()[1]
    last_smGraph = v_lines_smGraph[-1].split()[1]

    # Creating dictionaries for the edges in both graphs
    lg_edges = {i: [] for i in range(int(last_lgGraph)+1)}
    sm_edges = {i: [] for i in range(int(last_smGraph)+1)}

    # This loop matches the edges in the larger graph and stores them in a dictionary
    for line in e_lines_lgGraph:
        num = line.split()
        if (lg_edges[int(num[1])] is None):
            lg_edges[int(num[1])] = [int(num[2]), lg_v[int(num[2])], num[3]]
        else:
            lg_edges[int(num[1])].append(
                [int(num[2]), lg_v[int(num[2])], num[3]])

    # This loop matches the edges in the smaller graph and stores them in a dictionary
    for line in e_lines_smGraph:
        num = line.split()
        if (sm_edges[int(num[1])] is None):
            #  sm_edges[int(num[1])] = (int(num[2]),num[3])
            sm_edges[int(num[1])] = [int(num[2]), sm_v[int(num[2])], num[3]]
        else:
            # sm_edges[int(num[1])].append((int(num[2]),num[3]))
            sm_edges[int(num[1])].append(
                [int(num[2]), sm_v[int(num[2])], num[3]])

    # Sorting the edge lists for each vertex in both dictionaries
    for key in lg_edges:
        values = lg_edges[key]
        values.sort(key=lambda x: x[1])

    for key in sm_edges:
        values = sm_edges[key]
        values.sort(key=lambda x: x[1])

    # search for the first occurence of the node
    search_string = sm_v[0]
    found_search = False
    foundV_key = 0

    # Looping through all nodes in the larger graph and searching for a matching node
    # to check the possibility of finding a subgraph
    for key, value in lg_v.items():
        if value == search_string:
            foundV_key = key
            found_search = parallel_bfs(lg_edges, sm_edges, foundV_key)
            if (found_search):
                break

    # If no matching node was found or the graphs are not subgraphs, return
    if (not found_search):
        # print(f'The Two graphs are NOT subgraph')
        return False
    else:
        # print(f'found a subgraph')
        return True


def mine_frequent_subgraphs(frequent_subgraphs):
    # sorts from the smaller to larger graphs
    # print("frequent_subgraphs", len(frequent_subgraphs))
    frequent_subgraphs.sort(key=lambda x: len(x))
    # print(len(frequent_subgraphs))
    sml_pointer = 0
    lg_pointer = len(frequent_subgraphs) - 1

    while sml_pointer < len(frequent_subgraphs):
        sml_pointer_temp = sml_pointer
        while sml_pointer < lg_pointer:
            # print('small graph', frequent_subgraphs[sml_pointer])
            # print('large graph', frequent_subgraphs[lg_pointer])
            if representing_trees(frequent_subgraphs[lg_pointer], frequent_subgraphs[sml_pointer]):
                # print('found a subgraph-----------------------------')
                frequent_subgraphs.pop(sml_pointer)
                lg_pointer = len(frequent_subgraphs) - 1
                # print(frequent_subgraphs)
            else:
                # sml_pointer += 1
                lg_pointer -= 1
        sml_pointer = sml_pointer_temp+1
        lg_pointer = len(frequent_subgraphs) - 1
        # print('sm',sml_pointer)
        # print('lm',lg_pointer)

    return frequent_subgraphs


def maximal_frequent_subgraph(extracted_subgraphs):
    # print("extracted_subgraphs", len(extracted_subgraphs))

    fg = mine_frequent_subgraphs(extracted_subgraphs)
    # print("len fg")

    # This removes the lines that doesn't start with v or e
    for i in range(len(fg)):
        lines = fg[i].split('\n')
        for line in lines.copy():
            if not line or line[0] not in ["v", "e"]:
                if line.startswith('where:'):
                    where_str = line[8:-1]
                    where_arr = where_str.split(', ')
                    where_arr = [int(val) for val in where_arr]
                    # print(where_arr)
                    where_code_output.append(where_arr)
                lines.remove(line)
        fg[i] = '\n'.join(lines)
    # print(fg)
    # print("maximal_frequent_subgraph")
    return fg


def parse_ast(nodes, edges):
    # Create a dictionary of nodes
    ex = ''
    root = ast.parse(ex)
    node_type = ''
    node_id = -1
    ast_nodes = {}
    for node in nodes:
        # print(node)
        # Parse the node ID and type
        node_id = node_id+1
        node_type = node

        if node_type.startswith('Name#id'):
            # Parse the name and context of Name nodes
            name = node_type[8:]
            ast_node = ast.Name(id=name, ctx=ast.Load())
        elif node_type == 'Name':
            ast_node = ast.Name(id='PLACEHOLDER', ctx=ast.Load())
        # elif node_type.startswith('Attribute#attr'):
        #     attr = node_type[15:]
        #     ast_node = ast.Attribute(value=ast.Name('PLACEHOLDER',None), attr=attr, ctx=ast.Load())
        elif node_type == 'Call':
            ast_node = ast.Call(func=ast.Name(
                'PLACEHOLDER', None), args=[], keywords=[])
        elif node_type == 'Assign':
            ast_node = ast.Assign(targets=[], value=None)

        elif node_type == 'Load':
            ast_node = ast.Load()
        elif node_type == 'Store':
            ast_node = ast.Store()
        elif node_type == 'Del':
            ast_node = ast.Del()

        elif node_type == 'Import':
            ast_node = ast.Import(names=[])
        elif node_type.startswith('ImportFrom'):
            module_name = node_type[18:]
            # print('module_name',module_name)
            ast_node = ast.ImportFrom(module=module_name, names=[], level=0)

        elif node_type == 'Add':
            ast_node = ast.Add()
        elif node_type == 'Sub':
            ast_node = ast.Sub()
        elif node_type == 'Mult':
            ast_node = ast.Mult()
        elif node_type == 'MatMult':
            ast_node = ast.MatMult()
        elif node_type == 'Div':
            ast_node = ast.Div()
        elif node_type == 'Mod':
            ast_node = ast.Mod()
        elif node_type == 'Pow':
            ast_node = ast.Pow()
        elif node_type == 'LShift':
            ast_node = ast.LShift()
        elif node_type == 'RShift':
            ast_node = ast.RShift()
        elif node_type == 'BitOr':
            ast_node = ast.BitOr()
        elif node_type == 'BitXor':
            ast_node = ast.BitXor()
        elif node_type == 'BitAnd':
            ast_node = ast.BitAnd()
        elif node_type == 'FloorDiv':
            ast_node = ast.FloorDiv()
        elif node_type == 'Eq':
            ast_node = ast.Eq()
        elif node_type == 'NotEq':
            ast_node = ast.NotEq()
        elif node_type == 'Lt':
            ast_node = ast.Lt()
        elif node_type == 'LtE':
            ast_node = ast.LtE()
        elif node_type == 'Gt':
            ast_node = ast.Gt()
        elif node_type == 'GtE':
            ast_node = ast.GtE()
        elif node_type == 'Is':
            ast_node = ast.Is()
        elif node_type == 'IsNot':
            ast_node = ast.IsNot()
        elif node_type == 'In':
            ast_node = ast.In()
        elif node_type == 'NotIn':
            ast_node = ast.NotIn()

        elif node_type == 'BinOp':
            ast_node = ast.BinOp(left=None, op=None, right=None)

        elif node_type.startswith('alias'):
            first_eq_idx = node_type.find("=")
            next_char_idx = node_type.find("#", first_eq_idx)
            if next_char_idx == -1:
                next_char_idx = len(node_type)
            elif "\n" in node_type[first_eq_idx:next_char_idx]:
                next_char_idx = node_type.find("\n", first_eq_idx)

            second_eq_idx = node_type.find("=", first_eq_idx + 1)
            name = node_type[first_eq_idx + 1:next_char_idx].strip()
            if second_eq_idx == -1:
                ast_node = ast.alias(name, None)
            else:
                asname = node_type[second_eq_idx + 1:].strip()
                ast_node = ast.alias(name, asname)
    ################# DINA ##################################
        elif node_type == 'BoolOp':
            ast_node = ast.BoolOp(op=ast.And(), values=[])
        elif node_type == 'UnaryOp':
            ast_node = ast.UnaryOp(op=ast.UAdd(), operand=None)
        elif node_type == 'And':
            ast_node = ast.And()
        elif node_type == 'Not':
            ast_node = ast.Not()
        elif node_type == 'UAdd':
            ast_node = ast.UAdd()
        elif node_type == 'USub':
            ast_node = ast.USub()
        elif node_type == 'Invert':
            ast_node = ast.Invert()
        elif node_type == 'Or':
            ast_node = ast.Or()
        elif node_type == 'NamedExpr':
            ast_node = ast.NamedExpr(target=None, value=None)
        elif node_type == 'Lambda':
            ast_node = ast.Lambda(args=ast.arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=None)
        elif node_type == 'IfExp':
            ast_node = ast.IfExp(test=None, body=None, orelse=None)
        elif node_type == 'Dict':
            ast_node = ast.Dict(keys=[], values=[])
        elif node_type == 'Set':
            ast_node = ast.Set(elts=[])
        elif node_type == 'ListComp':
            ast_node = ast.ListComp(elt=None, generators=[])
        elif node_type == 'SetComp':
            ast_node = ast.SetComp(elt=None, generators=[])
        elif node_type == 'DictComp':
            ast_node = ast.DictComp(key=None, value=None, generators=[])
        elif node_type == 'GeneratorExp':
            ast_node = ast.GeneratorExp(elt=None, generators=[])
        elif node_type == 'comprehension':
            ast_node = ast.comprehension(
                target=None, iter=None, ifs=[], is_async=False)
        elif node_type == 'Compare':
            ast_node = ast.Compare(left=None, ops=[], comparators=[])

        elif node_type.startswith('FunctionDef'):
            func_name = node_type.split('=')[1]
            ast_node = ast.FunctionDef(name=func_name, args=ast.arguments(posonlyargs=[], args=[
            ], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[], decorator_list=[])
        elif node_type.startswith('AsyncFunctionDef'):
            func_name = node_type.split('=')[1]
            ast_node = ast.FunctionDef(name=func_name, args=ast.arguments(posonlyargs=[], args=[
            ], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[], decorator_list=[])
        elif node_type == 'Expr':
            ast_node = ast.Expr(ast.Name(id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type.startswith('Constant'):
            tmp = node_type.split('=')[1]
            value_node = tmp.split('#')[0]
            kind_node = None
            if len(node_type.split('=')) > 2:
                tmp = node_type.split('=')[2]
                kind_node = tmp.split('#')[0]
            # print(value_node, kind_node)
            if (value_node.isdigit()):
                value_node = int(value_node)
            ast_node = ast.Constant(value=value_node, kind=kind_node)
        elif node_type == 'List':
            ast_node = ast.List(elts=[], ctx=ast.Load())
        elif node_type == 'Module':
            # print('creating Module')
            ast_node = ast.Module(body=[], type_ignores=[])
        elif node_type == 'arguments':
            ast_node = ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[
            ], kw_defaults=[], kwarg=None, defaults=[])
        elif node_type == 'arg':
            ast_node = ast.arg(arg='PLACEHOLDER',
                               annotation=None, type_comment=None)
        elif node_type.startswith('ClassDef'):
            class_name = node_type.split('=')[1]
            ast_node = ast.ClassDef(
                name=class_name, bases=[], keywords=[], body=[], decorator_list=[])
        elif node_type.startswith('Attribute'):
            next_char_idx = node_type.find("#")
            if next_char_idx == -1:
                attr_name = 'PLACEHOLDER'
            else:
                attr_name = node_type.split('=')[1]
            ast_node = ast.Attribute(value=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), attr=attr_name, ctx=ast.Load())
        elif node_type.startswith('JoinedStr'):
            ast_node = ast.JoinedStr(values=[])
        elif node_type.startswith('FormattedValue'):
            conv_value = node_type.split('=')[1]
            ast_node = ast.JoinedStr(
                values=[], conversion=conv_value, format_spec=None)
        elif node_type.startswith('Return'):
            ast_node = ast.Return(value=None)
        elif node_type == 'Delete':
            ast_node = ast.Delete(targets=[])
        elif node_type == 'Del':
            ast_node = ast.Del()
        elif node_type == 'AugAssign':
            ast_node = ast.AugAssign(target=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), op=None, value=None)
        elif node_type.startswith('AnnAssign'):
            simple_val = node_type.split('=')[1]
            ast_node = ast.AnnAssign(target=ast.Name(id='PLACEHOLDER', ctx=ast.Load(
            )), annotation=ast.Name(id='Type', ctx=ast.Load()), value=None, simple=simple_val)
        elif node_type == 'For':
            ast_node = ast.For(target=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), iter=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[], type_comment=None)
        elif node_type == 'AsyncFor':
            ast_node = ast.AsyncFor(target=ast.Name(id='PLACEHOLDER', ctx=ast.Load()), iter=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[], type_comment=None)
        elif node_type == 'While':
            ast_node = ast.While(test=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), body=[], orelse=[])
        elif node_type == 'If':
            ast_node = ast.If(test=ast.Name(id='PLACEHOLDER',
                              ctx=ast.Load()), body=[], orelse=[])
        elif node_type == 'With':
            ast_node = ast.With(items=[], body=[], type_comment=None)
        elif node_type == 'AsyncWith':
            ast_node = ast.AsyncWith(items=[], body=[], type_comment=None)
        elif node_type == 'withitem':
            ast_node = ast.withitem(context_expr=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), optional_vars=None)
        elif node_type == 'Raise':
            ast_node = ast.Raise(exc=None, cause=None)
        elif node_type == 'Try':
            ast_node = ast.Try(body=[], handlers=[], orelse=[], finalbody=[])
        elif node_type.startswith('ExceptHandler'):
            next_char_idx = node_type.find("#")
            if (next_char_idx == -1):
                ast_node = ast.ExceptHandler(type=None, name=None, body=[])
            else:
                except_name = node_type.split('=')[1]
                ast_node = ast.ExceptHandler(
                    type=None, name=except_name, body=[])
        elif node_type == 'Assert':
            ast_node = ast.Assert(test=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), msg=None)
        elif node_type.startswith('Global'):
            placeholders_count = int(node_type.split('=')[1])
            ast_node = ast.Global(names=[])
            while placeholders_count > 0:
                ast_node.names.append('PLACEHOLDER')
                placeholders_count -= 1
        elif node_type.startswith('Nonlocal'):
            placeholders_count = int(node_type.split('=')[1])
            ast_node = ast.Nonlocal(names=[])
            while placeholders_count > 0:
                ast_node.names.append('PLACEHOLDER')
                placeholders_count -= 1
        elif (node_type == "Pass"):
            ast_node = ast.Pass()
        elif (node_type == "Break"):
            ast_node = ast.Break()
        elif (node_type == "Continue"):
            ast_node = ast.Continue()
        elif node_type == 'Await':
            ast_node = ast.Await(value=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type == 'Yield':
            ast_node = ast.Yield(value=None)
        elif node_type == 'YieldFrom':
            ast_node = ast.YieldFrom(value=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()))
        elif node_type == 'Subscript':
            ast_node = ast.Subscript(value=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), slice=None, ctx=ast.Load())
        elif node_type == 'Tuple':
            ast_node = ast.Tuple(elts=[], ctx=ast.Load())
        elif node_type == 'Slice':
            ast_node = ast.Slice(lower=None, upper=None, step=None)
        elif node_type == 'Starred':
            ast_node = ast.Starred(value=ast.Name(
                id='PLACEHOLDER', ctx=ast.Load()), ctx=ast.Load())
        elif node_type.startswith('keyword'):
            next_char_idx = node_type.find("#")
            if (next_char_idx == -1):
                ast_node = ast.keyword(value=ast.Name(
                    id='PLACEHOLDER', ctx=ast.Load()))
            else:
                arg_name = node_type.split('=')[1]
                ast_node = ast.keyword(arg=arg_name, value=ast.Name(
                    id='PLACEHOLDER', ctx=ast.Load()))

        else:
            raise ValueError(f"Invalid node type: {node_type}")
        ast_nodes[node_id] = ast_node

    # Create the AST by adding edges
    # print('created nodes',ast_nodes)

# EDGES #########################################################################3
    for parent_id, child_id, edge_type in edges:
        parent_node = ast_nodes[parent_id]
        child_node = ast_nodes[child_id]
        # print('p',ast.dump(parent_node))
        # print('c',ast.dump(child_node))

        if isinstance(parent_node, ast.Call):
            # print('EDGE TYPE',edge_type)
            if edge_type.startswith('arg'):
                # Add the child node as an argument to the Call node
                parent_node.args.append(child_node)
            elif edge_type == 'func':
                # Set the child node as the function of the Call node
                parent_node.func = child_node
            elif edge_type.startswith('keywords'):
                # Add the child node as a keyword argument to the Call node
                key, value = child_node.arg, child_node.value
                parent_node.keywords.append(ast.keyword(arg=key, value=value))
            # print('FOUND call',ast.dump(parent_node))
            # print('\n')

        elif isinstance(parent_node, ast.Assign):
            # Add the child node as a target or value of the Assign node
            #ast.Assign(targets, value, type_comment)
            # print('assign edge type: ', edge_type)
            if edge_type.startswith('targets'):
                parent_node.targets.append(child_node)
            elif edge_type.startswith('value'):
                parent_node.value = child_node
            else:
                raise ValueError(f"Invalid edge: {parent_id} -> {child_id}")
            # print('FOUND assign',ast.dump(parent_node))
            # print('\n')

        elif isinstance(parent_node, ast.Name):
            if edge_type == 'ctx':
                parent_node.ctx = child_node
                # print('FOUND name',ast.dump(parent_node))
                # print('\n')

        elif isinstance(parent_node, ast.Attribute):
            # print('EDGE TYPE',edge_type)
            if edge_type == 'value':
                # Add the child node as an argument to the Call node
                parent_node.value = child_node
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
            # print('FOUND attr',ast.dump(parent_node))
            # print('\n')

        elif isinstance(parent_node, ast.Import):
            # Add the child node as a name of the Import node
            parent_node.names.append(ast.alias(child_node))

        elif isinstance(parent_node, ast.ImportFrom):
            # Set the child node as the module or name of the ImportFrom node
            if edge_type == 'module':
                parent_node.module = child_node
            elif edge_type == 'names':
                parent_node.names.append(child_node)
            elif edge_type == 'level':
                parent_node.level = child_node
            else:
                raise ValueError(f"Invalid edge: {parent_id} -> {child_id}")
        elif isinstance(parent_node,  ast.BinOp):
            # Set the child node as the left or right operand of the Add or BinOp node
            if edge_type == 'op':
                parent_node.op = child_node
            elif edge_type == 'right':
                parent_node.right = child_node
            elif edge_type == 'left':
                parent_node.left = child_node
            else:
                raise ValueError(f"Invalid edge: {parent_id} -> {child_id}")

        elif isinstance(parent_node, (ast.Add, ast.Sub, ast.Mult, ast.MatMult, ast.Div, ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd, ast.FloorDiv)):
            pass
        elif isinstance(parent_node, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn)):
            pass
        elif isinstance(parent_node,  ast.alias):
            pass
        elif isinstance(parent_node,  ast.Or):
            pass
        elif isinstance(parent_node,  ast.BoolOp):
            if edge_type == 'op':
                parent_node.op = child_node
            elif edge_type.startswith('values'):
                parent_node.values.append(child_node)
        elif isinstance(parent_node,  ast.NamedExpr):
            if edge_type == 'target':
                parent_node.target = child_node

            elif edge_type == 'value':
                parent_node.value = child_node
        elif isinstance(parent_node,  ast.UnaryOp):
            if edge_type == 'op':
                parent_node.op = child_node

            elif edge_type == 'operand':
                parent_node.operand = child_node
        elif isinstance(parent_node,  ast.Lambda):
            if edge_type .startswith('args'):
                parent_node.args = child_node
            elif edge_type == 'body':
                parent_node.body = child_node
        elif isinstance(parent_node,  ast.IfExp):
            if edge_type == 'test':
                parent_node.test = child_node
            elif edge_type == 'body':
                parent_node.body = child_node
            elif edge_type == 'orelse':
                parent_node.orelse = child_node
        elif isinstance(parent_node, ast.Dict):
            if edge_type.startswith('keys'):
                parent_node.keys.append(child_node)
            elif edge_type.startswith('values'):
                parent_node.values.append(child_node)
        elif isinstance(parent_node, ast.Set):
            if edge_type.startswith('elts'):
                parent_node.elts.append(child_node)
        elif isinstance(parent_node, ast.ListComp):
            if edge_type == 'elt':
                parent_node.elt = child_node
            elif edge_type == 'generators':
                parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.SetComp):
            if edge_type == 'elt':
                parent_node.elt = child_node
            elif edge_type == 'generators':
                parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.DictComp):
            if edge_type == 'key':
                parent_node.key = child_node
            elif edge_type == 'value':
                parent_node.value = child_node
            elif edge_type == 'generators':
                parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.GeneratorExp):
            if edge_type == 'elt':
                parent_node.elt = child_node
            elif edge_type == 'generators':
                parent_node.generators.append(child_node)
        elif isinstance(parent_node, ast.comprehension):
            if edge_type == 'target':
                parent_node.target = child_node
            elif edge_type == 'iter':
                parent_node.iter = child_node
            elif edge_type.startswith('ifs'):
                parent_node.ifs.append(child_node)
            elif edge_type == 'is_async':
                parent_node.is_async = child_node
        elif isinstance(parent_node, ast.Compare):
            if edge_type == 'left':
                parent_node.left = child_node
            elif edge_type == 'ops':
                parent_node.ops.append(child_node)
            elif edge_type == 'comparators':
                parent_node.comparators.append(child_node)

                # xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX NOT CHECKED -MATCH XXXXXXXXXXXXXXXXXXXXX#########################3
        # elif isinstance(parent_node, (ast.MatchValue, ast.MatchSingleton, ast.MatchStar, ast.MatchAs)):
        #     if edge_type == 'value':
        #         parent_node.value = child_node
        #     elif edge_type == 'pattern':
        #         parent_node.pattern = child_node
        #     elif edge_type == 'name':
        #         parent_node.name = child_node
        # elif isinstance(parent_node, ast.MatchSequence):
        #   if edge_type == 'patterns':
        #       parent_node.patterns = child_node
        # elif isinstance(parent_node, ast.MatchMapping):
        #   if edge_type == 'keys':
        #       parent_node.keys = child_node
        #   elif edge_type == 'patterns':
        #       parent_node.patterns = child_node
        #   elif edge_type == 'rest':
        #       parent_node.rest = child_node
        # elif isinstance(parent_node, ast.MatchClass):
        #   if edge_type == 'cls':
        #       parent_node.cls = child_node
        #   elif edge_type == 'patterns':
        #       parent_node.patterns = child_node
        #   elif edge_type == 'kwd_attrs':
        #       parent_node.kwd_attrs = child_node
        #   elif edge_type == 'kwd_patterns':
        #       parent_node.kwd_patterns = child_node

        ###################### his is the new added nodes MENNA ########################
        elif isinstance(parent_node,  ast.FunctionDef) or isinstance(parent_node,  ast.AsyncFunctionDef):
            if edge_type.startswith('args'):
                parent_node.args = child_node
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type == 'decorator_list':
                parent_node.decorator_list.append(child_node)
            elif edge_type == 'returns':
                parent_node.returns = child_node
        elif isinstance(parent_node,  ast.Expr):
            parent_node.value = child_node
        elif isinstance(parent_node,  ast.Constant):
            pass
        elif isinstance(parent_node,  ast.List):
            if edge_type.startswith('elts'):
                # print('appending children', ast.dump(child_node))
                parent_node.elts.append(child_node)
                # print('parent after append', ast.dump(parent_node))
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Module):
            if edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type == 'type_ignores':
                parent_node.type_ignores.append(child_node)
            root = parent_node
        elif isinstance(parent_node, ast.arguments):
            if edge_type == 'posonlyargs':
                parent_node.posonlyargs.append(child_node)
            elif edge_type.startswith('args'):
                # print('adding args to argument', ast.dump(child_node))
                parent_node.args.append(child_node)
            elif edge_type == 'vararg':
                parent_node.vararg = child_node
            elif edge_type == 'kwonlyargs':
                parent_node.kwonlyargs.append(child_node)
            elif edge_type == 'kw_defaults':
                parent_node.kw_defaults.append(child_node)
            elif edge_type == 'kwarg':
                parent_node.kwarg = child_node
            elif edge_type == 'defaults':
                parent_node.defaults.append(child_node)
        elif isinstance(parent_node, ast.arg):
            if edge_type == 'annotation':
                parent_node.annotation = child_node
            elif edge_type == 'type_comment':
                parent_node.type_comment = child_node
        elif isinstance(parent_node, ast.ClassDef):
            if edge_type == 'bases':
                parent_node.bases.append(child_node)
            elif edge_type.startswith('keywords'):
                parent_node.keywords.append(child_node)
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type == 'decorator_list':
                parent_node.decorator_list.append(child_node)
        elif isinstance(parent_node, ast.Attribute):
            if edge_type == 'name':
                parent_node.name = child_node
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
        elif isinstance(parent_node, ast.JoinedStr):
            if edge_type == 'values':
                parent_node.values.append(child_node)
        elif isinstance(parent_node, ast.FormattedValue):
            if edge_type == 'values':
                parent_node.values.append(child_node)
            elif edge_type == 'format_spec':
                parent_node.format_spec = child_node
        elif isinstance(parent_node, ast.Return):
            if edge_type == 'value':
                parent_node.value = child_node
        elif isinstance(parent_node, ast.Delete):
            if edge_type.startswith('targets'):
                parent_node.targets.append(child_node)
        elif isinstance(parent_node,  ast.Del):
            pass
        elif isinstance(parent_node, ast.AugAssign):
            if edge_type == 'target':
                parent_node.target = child_node
            elif edge_type == 'op':
                parent_node.op = child_node
            elif edge_type == 'value':
                parent_node.value = child_node
        elif isinstance(parent_node, ast.AnnAssign):
            if edge_type == 'target':
                parent_node.target = child_node
            elif edge_type == 'annotation':
                parent_node.op = child_node
            elif edge_type == 'value':
                parent_node.value = child_node
        elif isinstance(parent_node, ast.For) or isinstance(parent_node, ast.AsyncFor):
            if edge_type == 'target':
                parent_node.target = child_node
            elif edge_type == 'iter':
                parent_node.iter = child_node
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type.startswith('orelse'):
                parent_node.orelse.append(child_node)
        elif isinstance(parent_node, ast.While) or isinstance(parent_node, ast.If):
            if edge_type == 'test':
                parent_node.test = child_node
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type.startswith('orelse'):
                parent_node.orelse.append(child_node)
        elif isinstance(parent_node, ast.With) or isinstance(parent_node, ast.AsyncWith):
            if edge_type.startswith('items'):
                parent_node.items.append(child_node)
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
        elif isinstance(parent_node, ast.withitem):
            if edge_type == 'context_expr':
                parent_node.context_expr = child_node
            elif edge_type == 'optional_vars':
                parent_node.optional_vars = child_node
        elif isinstance(parent_node, ast.Raise):
            if edge_type == 'exc':
                parent_node.exc = child_node
            elif edge_type == 'cause':
                parent_node.cause = child_node
        elif isinstance(parent_node, ast.ExceptHandler):
            if edge_type == 'type':
                parent_node.type = child_node
            elif edge_type.startswith('body'):
                parent_node.body.append(child_node)
        elif isinstance(parent_node, ast.Try):
            if edge_type.startswith('body'):
                parent_node.body.append(child_node)
            elif edge_type.startswith('handlers'):
                parent_node.handlers.append(child_node)
            elif edge_type.startswith('orelse'):
                parent_node.orelse.append(child_node)
            elif edge_type.startswith('finalbody'):
                parent_node.finalbody.append(child_node)
        elif isinstance(parent_node, ast.Assert):
            if edge_type == 'test':
                parent_node.test = child_node
            elif edge_type == 'msg':
                parent_node.msg = child_node
        elif isinstance(parent_node, ast.Global) or isinstance(parent_node, ast.Nonlocal):
            pass
        elif isinstance(parent_node, ast.Pass) or isinstance(parent_node, ast.Break) or isinstance(parent_node, ast.Continue):
            pass
        elif isinstance(parent_node, ast.Await) or isinstance(parent_node, ast.Yield) or isinstance(parent_node, ast.YieldFrom):
            if edge_type == 'value':
                parent_node.value = child_node
        elif isinstance(parent_node, ast.Subscript):
            if edge_type == 'value':
                parent_node.value = child_node
            elif edge_type == 'slice':
                parent_node.slice = child_node
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Tuple):
            if edge_type.startswith('elts'):
                parent_node.elts.append(child_node)
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
        elif isinstance(parent_node, ast.Slice):
            if edge_type == 'lower':
                parent_node.lower = child_node
            elif edge_type == 'upper':
                parent_node.upper = child_node
            elif edge_type == 'step':
                parent_node.step = child_node
        elif isinstance(parent_node, ast.Starred):
            if edge_type == 'value':
                parent_node.value = child_node
            elif edge_type == 'ctx':
                parent_node.ctx = child_node
        elif isinstance(parent_node, ast.keyword):
            if edge_type == 'value':
                parent_node.value = child_node

        else:
            raise ValueError(f"Invalid parent node type: {type(parent_node)}")

    # Create the root node of the AST
    if (not isinstance(ast_nodes[0], ast.Module)):
        root = ast.Module(body=[ast_nodes[0]])
    # Fix missing locations in the AST
    ast.fix_missing_locations(root)

    return root


def output_code(fg):
    # print("output code", len(fg))
    for index, tree in enumerate(fg):
        lines = tree.split('\n')
        # print(tree)
        nodes = []
        edges = []

        # Iterate over the lines and parse the nodes and edges
        for line in lines:
            if line.startswith('v '):
                # print(line.split(' '))
                _, index, node = line.split(' ')
                nodes.append(node)
            elif line.startswith('e '):
                _, source, target, edge_type = line.split(' ')
                edges.append((int(source), int(target), edge_type))

        # print('Nodes:', nodes)
        # print('Edges:', edges)
        root = parse_ast(nodes, edges)
        # print(parse_ast(nodes, edges))
        # ast.fix_missing_locations(root)
        print('ast', ast.dump(root))
        ast.dump(root)
        print(astor.to_source(root))
        code_output.append(astor.to_source(root))
    # print(len(code_output))
    return code_output


def main():
    # content = request.json
    # print(content['api'])
    api = input('')
    read_dir(api)
    snippets_to_ast()
    ast_to_gspan()
    common_patterns()
    extracted_subgraphs2 = array_of_patterns()
    fg = maximal_frequent_subgraph(extracted_subgraphs2)
    print(output_code(fg))
    return output_code(fg)


if __name__ == '__main__':
    main()
