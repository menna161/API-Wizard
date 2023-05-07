import os
import random
import code
from typing import Dict
import tensorflow as tf
import numpy as np
from graphviz import Digraph
from tqdm import tqdm


@classmethod
def random_tree(cls, language_spec: str, min_num_values: int, max_num_values: int, **kwargs):
    'Generate a random, valid tree based on a language spec. Trees are\n    generated as NumPy arrays and can be converted to TensorFlow tensors later.\n    '
    SPEC = LanguageSpecs[language_spec]
    assert (SPEC['data_structure'] == 'tree'), f'can not make tree batch with {language_spec} because it is not for trees.'
    adj_list = []
    values_list = []
    value_tokens_list = []
    order_list = []
    NUM_VALUE_TOKENS = len(SPEC['value_tokens'])
    NON_VALUE_NODE_TYPES = [nt for nt in SPEC['node_types'] if (not nt.is_value)]
    NUM_NODE_VALUES = (len(NON_VALUE_NODE_TYPES) + NUM_VALUE_TOKENS)
    NUM_ORDER_INDICES = (1 + SPEC['max_children'])
    num_values = random.randint(min_num_values, max_num_values)
    values = []
    for val_num in range(num_values):
        adj = []
        val = np.zeros(NUM_NODE_VALUES, dtype=np.int32)
        val_idx = random.randint(0, (NUM_VALUE_TOKENS - 1))
        val[val_idx] = 1
        val_token = SPEC['value_tokens'][val_idx]
        order = np.zeros(NUM_ORDER_INDICES, dtype=np.int32)
        adj_list.append(adj)
        values_list.append(val)
        value_tokens_list.append(val_token)
        order_list.append(order)
    tree_stack = list(range(num_values))
    next_idx = len(tree_stack)
    while (len(tree_stack) != 1):
        node_type_i = random.randint(0, (len(NON_VALUE_NODE_TYPES) - 1))
        new_node_type = NON_VALUE_NODE_TYPES[node_type_i]
        child_select_num = min([len(tree_stack), random.randint(new_node_type.min_children, new_node_type.max_children)])
        valid_children = []
        for child_i in tree_stack:
            child_token = value_tokens_list[child_i]
            if (child_token not in new_node_type.parent_blacklist):
                valid_children.append(child_i)
            else:
                pass
        children = random.sample(tree_stack, k=child_select_num)
        for (o_i, child_i) in enumerate(children):
            if new_node_type.ordered_children:
                order_list[child_i][(o_i + 1)] = 1
            else:
                order_list[child_i][0] = 1
        p_adj = children
        p_val = np.zeros(NUM_NODE_VALUES, dtype=np.int32)
        p_val[(NUM_VALUE_TOKENS + node_type_i)] = 1
        p_val_token = new_node_type.token
        p_order = np.zeros(NUM_ORDER_INDICES, dtype=np.int32)
        adj_list.append(p_adj)
        values_list.append(p_val)
        value_tokens_list.append(p_val_token)
        order_list.append(p_order)
        for child_i in children:
            tree_stack.remove(child_i)
        tree_stack.append(next_idx)
        next_idx += 1
    order_list[(- 1)][0] = 1
    return (adj_list, values_list, value_tokens_list, order_list)
