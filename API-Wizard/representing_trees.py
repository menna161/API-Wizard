"""#Represent Gspan format in vertices and edges"""


def representing_trees(lgGraph, smGraph):

    # Clearing the vertex dictionaries
    lg_v = {}
    sm_v = {}
    lg_v.clear()
    sm_v.clear()
    # lg_v = {}
    # sm_v = {}

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

    # print('lgGraph', lgGraph)
    # print('smGraph', smGraph)

    # print('sm_v', sm_v)
    # print('lg_v', lg_v)

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

    # parallel_bfs_supgraphs_helper(lg_v, sm_v, lg_edges, sm_edges )

    return lg_v, sm_v, lg_edges, sm_edges
