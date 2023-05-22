import warnings
import numpy as np, os, sys, pandas as pd, csv, random, datetime
import torch, torch.nn as nn
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle as pkl
from sklearn import metrics
from sklearn import cluster
import faiss
import losses as losses
from scipy.special import comb
from graphviz import Digraph


def save_graph(opt, model):
    '\n    Generate Network Graph.\n    NOTE: Requires the installation of the graphviz library on you system.\n\n    Args:\n        opt:   argparse.Namespace, contains all training-specific parameters.\n        model: PyTorch Network, network for which the computational graph should be visualized.\n    Returns:\n        Nothing!\n    '
    inp = torch.randn((1, 3, 224, 224)).to(opt.device)
    network_output = model(inp)
    if isinstance(network_output, dict):
        network_output = network_output['Class']
    from graphviz import Digraph

    def make_dot(var, savename, params=None):
        '\n        Generate a symbolic representation of the network graph.\n        '
        if (params is not None):
            assert all((isinstance(p, Variable) for p in params.values()))
            param_map = {id(v): k for (k, v) in params.items()}
        node_attr = dict(style='filled', shape='box', align='left', fontsize='6', ranksep='0.1', height='0.6', width='1')
        dot = Digraph(node_attr=node_attr, format='svg', graph_attr=dict(size='40,10', rankdir='LR', rank='same'))
        seen = set()

        def size_to_str(size):
            return (('(' + ', '.join([('%d' % v) for v in size])) + ')')

        def add_nodes(var):
            replacements = ['Backward', 'Th', 'Cudnn']
            color_assigns = {'Convolution': 'orange', 'ConvolutionTranspose': 'lightblue', 'Add': 'red', 'Cat': 'green', 'Softmax': 'yellow', 'Sigmoid': 'yellow', 'Copys': 'yellow'}
            if (var not in seen):
                op1 = torch.is_tensor(var)
                op2 = ((not torch.is_tensor(var)) and (str(type(var).__name__) != 'AccumulateGrad'))
                text = str(type(var).__name__)
                for rep in replacements:
                    text = text.replace(rep, '')
                color = (color_assigns[text] if (text in color_assigns.keys()) else 'gray')
                if ('Pool' in text):
                    color = 'lightblue'
                if (op1 or op2):
                    if hasattr(var, 'next_functions'):
                        count = 0
                        for (i, u) in enumerate(var.next_functions):
                            if (str(type(u[0]).__name__) == 'AccumulateGrad'):
                                if (count == 0):
                                    attr_text = '\nParameter Sizes:\n'
                                attr_text += size_to_str(u[0].variable.size())
                                count += 1
                                attr_text += ' '
                        if (count > 0):
                            text += attr_text
                if op1:
                    dot.node(str(id(var)), size_to_str(var.size()), fillcolor='orange')
                if op2:
                    dot.node(str(id(var)), text, fillcolor=color)
                seen.add(var)
                if (op1 or op2):
                    if hasattr(var, 'next_functions'):
                        for u in var.next_functions:
                            if (u[0] is not None):
                                if (str(type(u[0]).__name__) != 'AccumulateGrad'):
                                    dot.edge(str(id(u[0])), str(id(var)))
                                    add_nodes(u[0])
                    if hasattr(var, 'saved_tensors'):
                        for t in var.saved_tensors:
                            dot.edge(str(id(t)), str(id(var)))
                            add_nodes(t)
        add_nodes(var.grad_fn)
        dot.save(savename)
        return dot
    if (not os.path.exists(opt.save_path)):
        raise Exception('No save folder {} available!'.format(opt.save_path))
    viz_graph = make_dot(network_output, ((opt.save_path + '/Network_Graphs') + '/{}_network_graph'.format(opt.arch)))
    viz_graph.format = 'svg'
    viz_graph.render()
    torch.cuda.empty_cache()
