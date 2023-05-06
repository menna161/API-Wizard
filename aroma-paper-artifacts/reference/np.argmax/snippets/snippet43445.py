import argparse
from argparse import RawTextHelpFormatter
import csv
import glob
import os
import shutil
from collections import defaultdict
from typing import List
import numpy as np
import open3d
import pandas as pd
import torch
from plyfile import PlyData
from sklearn.neighbors import BallTree
import sys
from pretty_print import pretty_print_arguments
from clear_folder import clear_folder


def process_frame(file_path: str, global_params: dict=None):
    premapping = global_params['mapping']
    original_mesh = open3d.read_triangle_mesh(file_path)
    original_mesh.compute_vertex_normals()
    if args.train:
        if (args.dataset in ['scannet']):
            labels_file_path = file_path.replace('.ply', '.labels.ply')
            vertex_labels = np.asarray(PlyData.read(labels_file_path)['vertex']['label'])
        elif (args.dataset in ['s3dis']):
            labels_file_path = file_path.replace('.ply', '.labels.npy')
            vertex_labels = np.load(labels_file_path)
        elif (args.dataset in ['matterport']):
            mapped_labels = premapping[PlyData.read(file_path)['face']['category_id']]
            mapped_labels[np.logical_not(np.isin(mapped_labels, MATTERPORT_ALLOWED_NYU_CLASSES))] = 0
            vertices = np.asarray(original_mesh.vertices)
            triangles = np.asarray(original_mesh.triangles)
            remapped_labels = MATTERPORT_CLASS_REMAP[mapped_labels].astype(int)
            vertex_labels = np.zeros((vertices.shape[0], 22), dtype=np.int)
            for row_id in range(triangles.shape[0]):
                for i in range(3):
                    vertex_labels[(triangles[row_id][i], remapped_labels[row_id])] += 1
            vertex_labels = np.argmax(vertex_labels, axis=1)
        original_vertices = np.column_stack((np.asarray(original_mesh.vertices), np.asarray(original_mesh.vertex_colors), np.asarray(original_mesh.vertex_normals), vertex_labels))
        if (args.dataset in ['scannet']):
            class_ids = original_vertices[(:, (- 1))].astype(int)
            class_ids[(class_ids > 40)] = 0
            original_vertices[(:, (- 1))] = SCANNET_CLASS_REMAP[class_ids]
    else:
        assert (args.dataset in ['scannet'])
        original_vertices = np.column_stack((np.asarray(original_mesh.vertices), np.asarray(original_mesh.vertex_colors), np.asarray(original_mesh.vertex_normals)))
        s_path = file_path.replace('.ply', '_size.txt')
        if (not os.path.isfile(s_path)):
            with open(s_path, 'w') as s_file:
                s_file.write(f'{original_vertices.shape[0]}')
    if (args.dataset in ['scannet']):
        subfolder = f"{file_path.split('/')[(- 2)]}"
        curr_dir = f'{args.out_path}{subfolder}'
    elif (args.dataset in ['matterport']):
        subfolder = f"{file_path.split('/')[(- 3)]}_{file_path.split('/')[(- 1)].replace('.ply', '')}"
        curr_dir = f'{args.out_path}{subfolder}'
    elif (args.dataset in ['s3dis']):
        subfolder = f"{file_path.split('/')[(- 3)]}_{file_path.split('/')[(- 2)]}"
        curr_dir = f'{args.out_path}{subfolder}'
    clear_folder(f'{curr_dir}/')
    coords = []
    edges_list = []
    edge_output = []
    traces = []
    curr_mesh = original_mesh
    curr_vertices = np.asarray(curr_mesh.vertices)
    edge_list_0 = edges_from_faces(np.asarray(curr_mesh.triangles))
    coords.append(curr_vertices)
    edges_list.append(edge_list_0)
    edge_output_0 = []
    for (key, group) in enumerate(edge_list_0):
        for elem in group:
            edge_output_0.append([key, elem])
    edge_output.append(np.array(edge_output_0))
    if (not args.vertex_clustering):
        curr_mesh_path = f'{curr_dir}/curr_mesh.ply'
        open3d.io.write_triangle_mesh(curr_mesh_path, curr_mesh)
    for level in range(len(args.level_params)):
        if args.vertex_clustering:
            (coords_l, trace_scatter, edge_list_l, edge_output_l) = vertex_clustering(coords[(- 1)], edges_list[(- 1)], float(args.level_params[level]))
        elif (not args.level_params[level].isdigit()):
            os.system(f'trimesh_clustering {curr_mesh_path} {curr_mesh_path} -s {args.level_params[level]} > /dev/null')
            curr_mesh = open3d.io.read_triangle_mesh(curr_mesh_path)
            curr_mesh.compute_vertex_normals()
            coords_l = np.asarray(curr_mesh.vertices)
            edge_list_l = edges_from_faces(np.asarray(curr_mesh.triangles))
            edge_output_0 = []
            for (key, group) in enumerate(edge_list_l):
                for elem in group:
                    edge_output_0.append([key, elem])
            edge_output_l = edge_output_0
            vh_ball_tree = BallTree(coords_l[(:, :3)])
            vh_trace = vh_ball_tree.query(np.asarray(coords[0][(:, :3)]), k=1)[1].flatten()
            trace_scatter = vh_trace
        else:
            (coords_l, edge_output_l, trace_scatter) = quadric_error_metric(curr_mesh_path, int(args.level_params[level]), old_vertices=coords[(- 1)])
            edge_list_l = None
        coords.append(coords_l)
        traces.append(trace_scatter)
        edges_list.append(edge_list_l)
        edge_output.append(np.array(edge_output_l))
    colors_labels = get_color_and_labels(original_vertices, coords)
    coords_color_labels = []
    for i in range(len(coords)):
        coords_color_labels.append(np.column_stack((coords[i], colors_labels[i])))
    clear_folder(f'{curr_dir}/')
    coords_color_labels = [torch.from_numpy(coords_color_labels[i]) for i in range(len(coords_color_labels))]
    pt_data = {}
    if args.train:
        vertices = [coords_color_labels[1][(:, :(- 1))].float()]
        vertices.extend([coords_color_labels[i][(:, :3)].float() for i in range(2, len(coords_color_labels))])
        labels = coords_color_labels[0][(:, (- 1))].long()
        pt_data['vertices'] = vertices
        pt_data['labels'] = labels
    else:
        vertices = [coords_color_labels[1].float()]
        vertices.extend([coords_color_labels[i][(:, :3)].float() for i in range(2, len(coords_color_labels))])
        pt_data['vertices'] = vertices
    pt_data['edges'] = [torch.from_numpy(edge_output[i]).long() for i in range(1, len(edge_output))]
    pt_data['traces'] = [torch.from_numpy(x).long() for x in traces]
    torch.save(pt_data, f'{curr_dir}.pt')
    shutil.rmtree(f'{curr_dir}/')
