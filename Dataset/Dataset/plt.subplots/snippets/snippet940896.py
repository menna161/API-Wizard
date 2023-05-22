import networkx as nx
import scipy.spatial
import scipy.stats
import numpy as np
import random
import utm
import copy
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import time
import math
import os
import sys
import argparse
import pandas as pd
import shapely.wkt
import apls_utils
import apls_plots
import osmnx_funcs
import graphTools
import wkt_to_G
import topo_metric
import sp_metric


def execute(output_name, gt_list, gp_list, root_list, im_loc_list=[], weight='length', speed_key='inferred_speed_mps', travel_time_key='travel_time_s', test_method='gt_json_prop_json', max_files=1000, linestring_delta=50, is_curved_eps=(10 ** 3), max_snap_dist=4, max_nodes=500, n_plots=10, min_path_length=10, topo_hole_size=4, topo_subgraph_radius=150, topo_interval=30, sp_length_buffer=0.05, use_pix_coords=False, allow_renaming=True, verbose=True, super_verbose=False):
    "\n    Compute APLS for the input data in gt_list, gp_list\n\n    Arguments\n    ---------\n    output_name : str\n        Output name in apls/outputs\n    weight : str\n        Edge key determining path length weights. Defaults to ``'length'``.\n    speed_key : str\n        Edge key for speed. Defaults to ``'inferred_speed_mps'``.\n    travel_time_key : str\n        Edge key for travel time. Defaults to ``'travel_time_s'``.\n    max_files : int\n        Maximum number of files to analyze. Defaults to ``1000``.\n    linestring_delta : float\n        Distance in meters between linestring midpoints. Defaults to ``50``.\n    is_curved_eps : float\n        Minumum curvature for injecting nodes (if curvature is less than this\n        value, no midpoints will be injected). If < 0, always inject points\n        on line, regardless of curvature.  Defaults to ``0.3``.\n    max_snap_dist : float\n        Maximum distance a node can be snapped onto a graph.\n        Defaults to ``4``.\n    max_nodes : int\n        Maximum number of gt nodes to inject midpoints.  If there are more\n        gt nodes than this, skip midpoints and use this number of points\n        to comput APLS.\n    n_plots : int\n        Number of graphs to create plots for. Defaults to ``10``.\n    min_path_length : float\n        Mimumum path length to consider for APLS. Defaults to ``10``.\n    topo_hole_size : float\n        Hole size for TOPO in meters. Defaults to ``4``.\n    topo_subgraph_radius : float\n        Radius to search for TOPO, in meters. Defaults to ``150.``\n    topo_interval : float\n        Spacing of points in meters to inject for TOPO. Defaults to ``30``.\n    sp_length_buffer : float\n        Fractional difference in lengths for SP metric. Defaults to ``0.05``.\n    use_pix_coords : boolean\n        Switch to use pixel coords for colculating lengths.\n        Defaults to ``False``.\n    allow_renaming : boolean\n        Switch to rename nodes when injecting nodes into graphs.\n        Defaulst to ``True``.\n    verbose : boolean\n        Switch to print relevant values to screen.  Defaults to ``False``.\n    super_verbose : boolean\n        Switch to print mucho values to screen.  Defaults to ``False``.\n\n    Returns\n    -------\n    None\n    "
    print('\n\n\nCompute Results...')
    C_arr = [['outroot', 'APLS', 'APLS_gt_onto_prop', 'APLS_prop_onto_gt', 'topo_tp_tot', 'topo_fp_tot', 'topo_fn_tot', 'topo_precision', 'topo_recall', 'topo_f1', 'sp_metric', 'tot_meters_gt', 'tot_meters_p']]
    title_fontsize = 4
    dpi = 200
    show_plots = False
    show_node_ids = True
    (fig_height, fig_width) = (6, 6)
    route_linewidth = 4
    source_color = 'red'
    target_color = 'green'
    valid_road_types = set([])
    outdir_base = os.path.join(path_apls, 'outputs')
    print('Outdir base:', outdir_base)
    outdir_base2 = os.path.join(outdir_base, str(output_name), ('weight=' + str(weight)), test_method)
    print('Outdir with weight:', outdir_base2)
    d_list = [outdir_base, outdir_base2]
    for p in d_list:
        if (not os.path.exists(p)):
            os.makedirs(p)
    t0 = time.time()
    for (i, [outroot, G_gt_init, G_p_init]) in enumerate(zip(root_list, gt_list, gp_list)):
        if (i >= max_files):
            break
        if (len(im_loc_list) > 0):
            im_loc = im_loc_list[i]
        else:
            im_loc = ''
        print('\n\n\n', (i + 1), '/', len(root_list), 'Computing:', outroot)
        t1 = time.time()
        print('len(G_gt_init.nodes():)', len(G_gt_init.nodes()))
        print('len(G_gt_init.edges():)', len(G_gt_init.edges()))
        print('len(G_p_init.nodes():)', len(G_p_init.nodes()))
        print('len(G_p_init.edges():)', len(G_p_init.edges()))
        print('\nMake gt, prop graphs...')
        if (len(G_gt_init.nodes()) < 500):
            (G_gt_cp, G_p_cp, G_gt_cp_prime, G_p_cp_prime, control_points_gt, control_points_prop, all_pairs_lengths_gt_native, all_pairs_lengths_prop_native, all_pairs_lengths_gt_prime, all_pairs_lengths_prop_prime) = make_graphs(G_gt_init, G_p_init, weight=weight, speed_key=speed_key, travel_time_key=travel_time_key, linestring_delta=linestring_delta, is_curved_eps=is_curved_eps, max_snap_dist=max_snap_dist, allow_renaming=allow_renaming, verbose=verbose)
        else:
            (G_gt_cp, G_p_cp, G_gt_cp_prime, G_p_cp_prime, control_points_gt, control_points_prop, all_pairs_lengths_gt_native, all_pairs_lengths_prop_native, all_pairs_lengths_gt_prime, all_pairs_lengths_prop_prime) = make_graphs_yuge(G_gt_init, G_p_init, weight=weight, speed_key=speed_key, travel_time_key=travel_time_key, max_nodes=max_nodes, max_snap_dist=max_snap_dist, allow_renaming=allow_renaming, verbose=verbose, super_verbose=super_verbose)
        if verbose:
            print('\nlen control_points_gt:', len(control_points_gt))
            if (len(G_gt_init.nodes()) < 200):
                print('G_gt_init.nodes():', G_gt_init.nodes())
            print('len G_gt_init.edges():', len(G_gt_init.edges()))
            if (len(G_gt_cp.nodes()) < 200):
                print('G_gt_cp.nodes():', G_gt_cp.nodes())
            print('len G_gt_cp.nodes():', len(G_gt_cp.nodes()))
            print('len G_gt_cp.edges():', len(G_gt_cp.edges()))
            print('len G_gt_cp_prime.nodes():', len(G_gt_cp_prime.nodes()))
            print('len G_gt_cp_prime.edges():', len(G_gt_cp_prime.edges()))
            print('\nlen control_points_prop:', len(control_points_prop))
            if (len(G_p_init.nodes()) < 200):
                print('G_p_init.nodes():', G_p_init.nodes())
            print('len G_p_init.edges():', len(G_p_init.edges()))
            if (len(G_p_cp.nodes()) < 200):
                print('G_p_cp.nodes():', G_p_cp.nodes())
            print('len G_p_cp.nodes():', len(G_p_cp.nodes()))
            print('len G_p_cp.edges():', len(G_p_cp.edges()))
            print('len G_p_cp_prime.nodes():', len(G_p_cp_prime.nodes()))
            if (len(G_p_cp_prime.nodes()) < 200):
                print('G_p_cp_prime.nodes():', G_p_cp_prime.nodes())
            print('len G_p_cp_prime.edges():', len(G_p_cp_prime.edges()))
            print('len all_pairs_lengths_gt_native:', len(dict(all_pairs_lengths_gt_native)))
            print('len all_pairs_lengths_gt_prime:', len(dict(all_pairs_lengths_gt_prime)))
            print('len all_pairs_lengths_prop_native', len(dict(all_pairs_lengths_prop_native)))
            print('len all_pairs_lengths_prop_prime', len(dict(all_pairs_lengths_prop_prime)))
        if (i < n_plots):
            res_dir = outdir
        else:
            res_dir = ''
        (C, C_gt_onto_prop, C_prop_onto_gt) = compute_apls_metric(all_pairs_lengths_gt_native, all_pairs_lengths_prop_native, all_pairs_lengths_gt_prime, all_pairs_lengths_prop_prime, control_points_gt, control_points_prop, min_path_length=min_path_length, verbose=verbose, res_dir=res_dir)
        print('APLS Metric = ', C)
        print('\nComputing TOPO Metric...')
        n_measurement_nodes = max_nodes
        topo_vals = topo_metric.compute_topo(G_gt_init, G_p_init, subgraph_radius=topo_subgraph_radius, interval=topo_interval, hole_size=topo_hole_size, n_measurement_nodes=n_measurement_nodes, x_coord='x', y_coord='y', allow_multi_hole=False, make_plots=False, verbose=False)
        (topo_tp_tot, topo_fp_tot, topo_fn_tot, topo_precision, topo_recall, topo_f1) = topo_vals
        print('TOPO Metric subgraph_radius, interval:', topo_subgraph_radius, topo_interval)
        print('TOPO Metric =', topo_vals, 'for', n_measurement_nodes, 'nodes, subgraph_radius =', topo_subgraph_radius)
        print('\nComputing sp Metric...')
        sp_n_routes = max_nodes
        (_, sp) = sp_metric.compute_sp(G_gt_init, G_p_init, x_coord='x', y_coord='y', weight=weight, query_radius=max_snap_dist, length_buffer=sp_length_buffer, n_routes=sp_n_routes, verbose=False, make_plots=False)
        print('sp_length_buffer:', sp_length_buffer)
        print('sp Metric =', sp, 'for', sp_n_routes, 'routes, length buffer =', sp_length_buffer)
        tot_meters_gt = 0
        for (itmp, (u, v, attr_dict)) in enumerate(G_gt_init.edges(data=True)):
            tot_meters_gt += attr_dict['length']
        print('Ground truth total length of edges (km):', (tot_meters_gt / 1000))
        G_gt_init.graph['Tot_edge_km'] = (tot_meters_gt / 1000)
        tot_meters_p = 0
        for (itmp, (u, v, attr_dict)) in enumerate(G_p_init.edges(data=True)):
            tot_meters_p += attr_dict['length']
        print('Proposal total length of edges (km):', (tot_meters_p / 1000))
        G_p_init.graph['Tot_edge_km'] = (tot_meters_p / 1000)
        f = open(os.path.join(outdir_base2, ((((((((((((str(output_name) + '_') + 'weight=') + str(weight)) + '_') + test_method) + 'output__max_snap=') + str(np.round(max_snap_dist, 2))) + 'm') + '_hole=') + str(np.round(topo_hole_size, 2))) + 'm') + '.txt')), 'w')
        f.write((('Ground Truth Nodes Snapped Onto Proposal Score: ' + str(C_gt_onto_prop)) + '\n'))
        f.write((('Proposal Nodes Snapped Onto Ground Truth Score: ' + str(C_prop_onto_gt)) + '\n'))
        f.write((('Total APLS Score: ' + str(C)) + '\n'))
        f.write((('TOPO vals - topo_tp_tot, topo_fp_tot, topo_fn_tot, topo_precision, topo_recall, topo_f1: ' + str(topo_vals)) + '\n'))
        f.write(('SP: ' + str(sp)))
        f.close()
        t2 = time.time()
        print('Total time to create graphs and compute metric:', (t2 - t1), 'seconds')
        C_arr.append([outroot, C, C_gt_onto_prop, C_prop_onto_gt, topo_tp_tot, topo_fp_tot, topo_fn_tot, topo_precision, topo_recall, topo_f1, sp, tot_meters_gt, tot_meters_p])
        if (i < n_plots):
            if ((len(G_gt_cp.nodes()) == 0) or (len(G_p_cp.nodes()) == 0)):
                continue
            max_extent = max(fig_height, fig_width)
            (xmin, xmax, ymin, ymax, dx, dy) = apls_utils._get_graph_extent(G_gt_cp)
            if (dx <= dy):
                fig_height = max_extent
                fig_width = max(1, (((1.0 * max_extent) * dx) / dy))
            else:
                fig_width = max_extent
                fig_height = max(1, (((1.0 * max_extent) * dy) / dx))
            if verbose:
                print('fig_width, fig_height:', fig_width, fig_height)
            (fig, ax) = osmnx_funcs.plot_graph(G_gt_init, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax = apls_plots.plot_node_ids(G_gt_init, ax, fontsize=4)
            ax.set_title('Ground Truth Graph', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'gt_graph.png'), dpi=dpi)
            plt.close('all')
            (fig0, ax0) = osmnx_funcs.plot_graph(G_gt_cp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax0 = apls_plots.plot_node_ids(G_gt_cp, ax0, fontsize=4)
            ax0.set_title('Ground Truth With Midpionts', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'gt_graph_midpoints.png'), dpi=dpi)
            plt.close('all')
            (fig, ax) = osmnx_funcs.plot_graph(G_gt_cp_prime, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax = apls_plots.plot_node_ids(G_gt_cp_prime, ax, fontsize=4)
            ax.set_title('Ground Truth Graph with Proposal Control Nodes', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'gt_graph_prop_control_points.png'), dpi=dpi)
            plt.close('all')
            Gtmp = G_gt_cp.copy()
            for (itmp, (u, v, key, data)) in enumerate(Gtmp.edges(keys=True, data=True)):
                try:
                    data.pop('geometry', None)
                except:
                    data[0].pop('geometry', None)
            (fig, ax) = osmnx_funcs.plot_graph(Gtmp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            ax.set_title('Ground Truth Graph (cp) without any geometry', size='x-small')
            plt.savefig(os.path.join(outdir, 'gt_without_geom.png'), dpi=dpi)
            plt.close('all')
            (fig, ax) = osmnx_funcs.plot_graph(G_p_init, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax = apls_plots.plot_node_ids(G_p_init, ax, fontsize=4)
            ax.set_title('Proposal Graph', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'prop_graph.png'), dpi=dpi)
            plt.close('all')
            (fig0, ax0) = osmnx_funcs.plot_graph(G_p_cp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax = apls_plots.plot_node_ids(G_p_cp, ax0, fontsize=4)
            ax0.set_title('Proposal With Midpionts', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'prop_graph_midpoints.png'), dpi=dpi)
            plt.close('all')
            (fig0, ax0) = osmnx_funcs.plot_graph(G_p_cp_prime, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            if show_node_ids:
                ax = apls_plots.plot_node_ids(G_p_cp_prime, ax0, fontsize=4)
            ax0.set_title('Proposal With Midpionts from GT', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'prop_graph_midpoints_gt_control_points.png'), dpi=dpi)
            plt.close('all')
            G_tmp = G_p_init.copy()
            (fig, ax3) = osmnx_funcs.plot_graph(G_tmp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            try:
                apls_plots._plot_buff(G_gt_init, ax3, buff=max_snap_dist, color='yellow', alpha=0.3, title='', title_fontsize=title_fontsize, outfile='', verbose=False)
            except:
                print('Cannot make buffer plot...')
            ax3.set_title('Propoal Graph with Ground Truth Buffer', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'prop_graph_plus_gt_buff.png'), dpi=dpi)
            plt.close('all')
            (fig, ax4) = osmnx_funcs.plot_graph(G_gt_init, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            try:
                apls_plots._plot_buff(G_p_init, ax4, buff=max_snap_dist, color='yellow', alpha=0.3, title='', title_fontsize=title_fontsize, outfile='', verbose=False)
            except:
                print('Cannot make buffer plot...')
            ax4.set_title('Ground Graph with Proposal Buffer', fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'gt_graph_plus_prop_buff.png'), dpi=dpi)
            plt.close('all')
            Gtmp = G_p_cp.copy()
            for (itmp, (u, v, key, data)) in enumerate(Gtmp.edges(keys=True, data=True)):
                try:
                    data.pop('geometry', None)
                except:
                    data[0].pop('geometry', None)
            (fig, ax) = osmnx_funcs.plot_graph(Gtmp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            ax.set_title('Proposal Graph (cp) without any geometry', size='x-small')
            plt.savefig(os.path.join(outdir, 'prop_cp_without_geom.png'), dpi=dpi)
            plt.close('all')
            Gtmp = G_p_init.copy()
            for (itmp, (u, v, key, data)) in enumerate(Gtmp.edges(keys=True, data=True)):
                try:
                    data.pop('geometry', None)
                except:
                    data[0].pop('geometry', None)
            (fig, ax) = osmnx_funcs.plot_graph(Gtmp, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
            ax.set_title('Proposal Graph without any geometry', size='x-small')
            plt.savefig(os.path.join(outdir, 'prop_without_geom.png'), dpi=dpi)
            plt.close('all')
            if (len(G_gt_cp.nodes()) < 200):
                print('G_gt_cp.nodes():', G_gt_cp.nodes())
            if (len(G_gt_cp_prime.nodes()) < 200):
                print('G_p_cp_prime.nodes():', G_gt_cp_prime.nodes())
            possible_sources = set(G_gt_cp.nodes()).intersection(set(G_p_cp_prime.nodes()))
            if (len(possible_sources) == 0):
                continue
            source = random.choice(list(possible_sources))
            possible_targets = (set(G_gt_cp.nodes()).intersection(set(G_p_cp_prime.nodes())) - set([source]))
            if (len(possible_targets) == 0):
                continue
            target = random.choice(list(possible_targets))
            print('source, target:', source, target)
            t0 = time.time()
            (lengths, paths) = nx.single_source_dijkstra(G_gt_cp, source=source, weight=weight)
            print('Time to calculate:', len(lengths), 'paths:', (time.time() - t0), 'seconds')
            try:
                (fig, ax) = osmnx_funcs.plot_graph_route(G_gt_cp, paths[target], route_color='yellow', route_alpha=0.8, orig_dest_node_alpha=0.3, orig_dest_node_size=120, route_linewidth=route_linewidth, orig_dest_node_color=target_color, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
                plen = np.round(lengths[target], 2)
            except:
                print('Proposal route not possible')
                (fig, ax) = plt.subplots()
                plen = (- 1)
            title = ('Ground Truth Graph, L = ' + str(plen))
            source_x = G_gt_cp.nodes[source]['x']
            source_y = G_gt_cp.nodes[source]['y']
            ax.scatter(source_x, source_y, color=source_color, s=75)
            t_x = G_gt_cp.nodes[target]['x']
            t_y = G_gt_cp.nodes[target]['y']
            ax.scatter(t_x, t_y, color=target_color, s=75)
            ax.set_title(title, fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'single_source_route_ground_truth.png'), dpi=dpi)
            plt.close('all')
            (lengths_prop, paths_prop) = nx.single_source_dijkstra(G_p_cp_prime, source=source, weight=weight)
            gt_set = set(lengths.keys())
            prop_set = set(lengths_prop.keys())
            missing_nodes = (gt_set - prop_set)
            print('Proposal route missing nodes:', missing_nodes)
            t0 = time.time()
            (lengths_ptmp, paths_ptmp) = nx.single_source_dijkstra(G_p_cp_prime, source=source, weight=weight)
            print('Time to calculate:', len(lengths), 'paths:', (time.time() - t0), 'seconds')
            try:
                (fig, ax) = osmnx_funcs.plot_graph_route(G_p_cp_prime, paths_ptmp[target], route_color='yellow', route_alpha=0.8, orig_dest_node_alpha=0.3, orig_dest_node_size=120, route_linewidth=route_linewidth, orig_dest_node_color=target_color, show=show_plots, close=False, fig_height=fig_height, fig_width=fig_width)
                plen = np.round(lengths_ptmp[target], 2)
            except:
                print('Proposal route not possible')
                (fig, ax) = plt.subplots()
                plen = (- 1)
            title = ('Proposal Graph, L = ' + str(plen))
            source_x = G_p_cp_prime.nodes[source]['x']
            source_y = G_p_cp_prime.nodes[source]['y']
            ax.scatter(source_x, source_y, color=source_color, s=75)
            t_x = G_p_cp_prime.nodes[target]['x']
            t_y = G_p_cp_prime.nodes[target]['y']
            ax.scatter(t_x, t_y, color=target_color, s=75)
            ax.set_title(title, fontsize=title_fontsize)
            plt.savefig(os.path.join(outdir, 'single_source_route_prop.png'), dpi=dpi)
            plt.close('all')
            if (len(im_loc_list) > 0):
                image_path = im_loc_list[i]
                if os.path.exists(image_path):
                    (gt_color, prop_color) = ('cyan', 'lime')
                    image_name = outroot
                    figname = os.path.join(outdir, 'overlaid.png')
                    _ = apls_plots._plot_gt_prop_graphs(G_gt_init, G_p_init, image_path, figsize=(16, 8), show_endnodes=True, width_key=2, width_mult=1, gt_color=gt_color, prop_color=prop_color, default_node_size=20, title=image_name, adjust=False, figname=figname, verbose=super_verbose)
            t2 = time.time()
            print('Total time to create graphs, compute metric, and plot:', (t2 - t0), 'seconds')
    print(('C_arr:', C_arr))
    tf = time.time()
    print(('Time to compute metric:', (tf - t0), 'seconds'))
    print(('N input images:', len(root_list)))
    means = np.mean(np.array(C_arr)[(1:, 1:)].astype(float), axis=0)
    C_arr.append((['means'] + list(means)))
    stds = np.std(np.array(C_arr)[(1:, 1:)].astype(float), axis=0)
    C_arr.append((['stds'] + list(stds)))
    path_csv = os.path.join(outdir_base2, (((((('scores__max_snap=' + str(np.round(max_snap_dist, 2))) + 'm') + '_hole=') + str(np.round(topo_hole_size, 2))) + 'm') + '.csv'))
    print('Save to csv:', path_csv)
    df = pd.DataFrame(C_arr[1:], columns=C_arr[0])
    print('len df:', len(df))
    df.to_csv(path_csv)
    print(('Tot APLS = np.mean(APLS_arr:', np.mean(df['APLS'].values)))
    return
