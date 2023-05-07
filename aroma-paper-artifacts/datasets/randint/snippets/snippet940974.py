import apls_utils
import apls
import os
import sys
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import osmnx_funcs

if (__name__ == '__main__'):
    n_measurement_nodes = 10
    x_coord = 'x'
    y_coord = 'y'
    weight = 'length'
    query_radius = 5
    length_buffer = 0.05
    n_routes = 500
    verbose = False
    run_all = True
    truth_dir = '/raid/cosmiq/spacenet/data/spacenetv2/AOI_2_Vegas_Test/400m/gt_graph_pkls'
    prop_dir = 'raid/cosmiq/basiss/inference_mod_new/results/rgb_test_sn_vegas/graphs'
    name_list = os.listdir(truth_dir)
    f = name_list[np.random.randint(len(name_list))]
    print(('f:', f))
    t0 = time.time()
    outroot = f.split('.')[0]
    print('\noutroot:', outroot)
    gt_file = os.path.join(truth_dir, f)
    prop_file = os.path.join(prop_dir, (outroot + '.gpickle'))
    G_gt_init = nx.read_gpickle(gt_file)
    G_gt_init1 = osmnx_funcs.simplify_graph(G_gt_init.to_directed()).to_undirected()
    G_gt_init = osmnx_funcs.project_graph(G_gt_init1)
    G_gt_init = apls.create_edge_linestrings(G_gt_init, remove_redundant=True, verbose=False)
    print(('G_gt_init.nodes():', G_gt_init.nodes()))
    (u, v) = G_gt_init.edges()[0]
    print(('random edge props:', G_gt_init.edge[u][v]))
    G_p_init = nx.read_gpickle(prop_file)
    G_p_init = apls.create_edge_linestrings(G_p_init, remove_redundant=True, verbose=False)
    t0 = time.time()
    print('\nComputing score...')
    (match_list, score) = compute_sp(G_gt_init, G_p_init, x_coord=x_coord, y_coord=y_coord, weight=weight, query_radius=query_radius, length_buffer=length_buffer, n_routes=n_routes, make_plots=True, verbose=verbose)
    print(('score:', score))
    print(('Time to compute score:', (time.time() - t0), 'seconds'))
    if run_all:
        t0 = time.time()
        plt.close('all')
        score_list = []
        match_list = []
        for (i, f) in enumerate(name_list):
            if (i == 0):
                make_plots = True
            else:
                make_plots = False
            outroot = f.split('.')[0]
            print('\n', i, '/', len(name_list), 'outroot:', outroot)
            gt_file = os.path.join(truth_dir, f)
            G_gt_init = nx.read_gpickle(gt_file)
            G_gt_init = apls.create_edge_linestrings(G_gt_init, remove_redundant=True, verbose=False)
            if (len(G_gt_init.nodes()) == 0):
                continue
            prop_file = os.path.join(prop_dir, (outroot + '.gpickle'))
            if (not os.path.exists(prop_file)):
                score_list.append(0)
                continue
            G_p_init0 = nx.read_gpickle(prop_file)
            G_p_init1 = osmnx_funcs.simplify_graph(G_p_init0.to_directed()).to_undirected()
            G_p_init = osmnx_funcs.project_graph(G_p_init1)
            G_p_init = apls.create_edge_linestrings(G_p_init, remove_redundant=True, verbose=False)
            (match_list_tmp, score) = compute_sp(G_gt_init, G_p_init, x_coord=x_coord, y_coord=y_coord, weight=weight, query_radius=query_radius, length_buffer=length_buffer, n_routes=n_routes, make_plots=make_plots, verbose=verbose)
            score_list.append(score)
            match_list.extend(match_list_tmp)
        sp_tot = ((1.0 * np.sum(match_list)) / len(match_list))
        print(('Total sp metric for', len(name_list), 'files:'))
        print(('  query_radius:', query_radius, 'length_buffer:', length_buffer))
        print(('  n_measurement_nodes:', n_measurement_nodes, 'n_routes:', n_routes))
        print(('  total time elapsed to compute sp and make plots:', (time.time() - t0), 'seconds'))
        print(('  total sp:', sp_tot))
