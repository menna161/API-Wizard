import os
import sys
import time
import numpy as np
import networkx as nx
import scipy.spatial
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, LineString
import apls
import apls_plots
import apls_utils
import osmnx_funcs

if (__name__ == '__main__'):
    n_measurement_nodes = 10
    subgraph_radius = 150
    interval = 30
    hole_size = 5
    x_coord = 'x'
    y_coord = 'y'
    allow_multi_hole = False
    make_plots = True
    run_all = True
    verbose = True
    truth_dir = '/raid/cosmiq/spacenet/data/spacenetv2/AOI_2_Vegas_Test/400m/gt_graph_pkls'
    prop_dir = 'raid/cosmiq/basiss/inference_mod_new/results/rgb_test_sn_vegas/graphs'
    name_list = os.listdir(truth_dir)
    f = name_list[np.random.randint(len(name_list))]
    f = 'AOI_2_Vegas_img150.pkl'
    print(('f:', f))
    t0 = time.time()
    outroot = f.split('.')[0]
    print('\noutroot:', outroot)
    gt_file = os.path.join(truth_dir, f)
    prop_file = os.path.join(prop_dir, (outroot + '.gpickle'))
    G_gt_init = nx.read_gpickle(gt_file)
    G_gt_init = apls.create_edge_linestrings(G_gt_init, remove_redundant=True, verbose=False)
    print(('G_gt_init.nodes():', G_gt_init.nodes()))
    G_p_init0 = nx.read_gpickle(prop_file)
    G_p_init1 = osmnx_funcs.simplify_graph(G_p_init0.to_directed()).to_undirected()
    G_p_init = osmnx_funcs.project_graph(G_p_init1)
    G_p_init = apls.create_edge_linestrings(G_p_init, remove_redundant=True, verbose=False)
    (tp_tot, fp_tot, fn_tot, precision, recall, f1) = compute_topo(G_gt_init, G_p_init, subgraph_radius=subgraph_radius, interval=interval, hole_size=hole_size, n_measurement_nodes=n_measurement_nodes, x_coord=x_coord, y_coord=y_coord, allow_multi_hole=allow_multi_hole, make_plots=make_plots, verbose=verbose)
    if run_all:
        t0 = time.time()
        (tp_tot_list, fp_tot_list, fn_tot_list) = ([], [], [])
        for (i, f) in enumerate(name_list):
            outroot = f.split('.')[0]
            print('\n', i, '/', len(name_list), 'outroot:', outroot)
            gt_file = os.path.join(truth_dir, f)
            G_gt_init = nx.read_gpickle(gt_file)
            G_gt_init = apls.create_edge_linestrings(G_gt_init, remove_redundant=True, verbose=False)
            if (len(G_gt_init.nodes()) == 0):
                continue
            prop_file = os.path.join(prop_dir, (outroot + '.gpickle'))
            if (not os.path.exists(prop_file)):
                tp_tot_list.append(0)
                fp_tot_list.append(0)
                fn_tot_list.append(len(G_gt_init.nodes()))
                continue
            G_p_init0 = nx.read_gpickle(prop_file)
            G_p_init1 = osmnx_funcs.simplify_graph(G_p_init0.to_directed()).to_undirected()
            G_p_init = osmnx_funcs.project_graph(G_p_init1)
            G_p_init = apls.create_edge_linestrings(G_p_init, remove_redundant=True, verbose=False)
            (tp, fp, fn, precision, recall, f1) = compute_topo(G_gt_init, G_p_init, subgraph_radius=subgraph_radius, interval=interval, hole_size=hole_size, n_measurement_nodes=n_measurement_nodes, x_coord=x_coord, y_coord=y_coord, allow_multi_hole=allow_multi_hole, make_plots=False, verbose=False)
            tp_tot_list.append(tp)
            fp_tot_list.append(fp)
            fn_tot_list.append(fn)
        tp_tot = np.sum(tp_tot_list)
        fp_tot = np.sum(fp_tot_list)
        fn_tot = np.sum(fn_tot_list)
        precision = (float(tp_tot) / float((tp_tot + fp_tot)))
        recall = (float(tp_tot) / float((tp_tot + fn_tot)))
        f1 = (((2.0 * precision) * recall) / (precision + recall))
        print(('Total TOPO metric for', len(name_list), 'files:'))
        print(('  hole_size:', hole_size, 'interval:', interval))
        print(('  subgraph_radius:', subgraph_radius, 'allow_multi_hole?', allow_multi_hole))
        print(('  total time elapsed to compute TOPO and make plots:', (time.time() - t0), 'seconds'))
        print(('  total precison:', precision))
        print(('  total recall:', recall))
        print(('  total f1:', f1))
