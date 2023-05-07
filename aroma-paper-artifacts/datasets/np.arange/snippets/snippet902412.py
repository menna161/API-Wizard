from transformers import BertTokenizer, BertModel, BertForMaskedLM
import os
import re
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
import numpy as np


def forward_as_init(self, num_nodes, network=None):
    if self.exists:
        print('Loading BERT embeddings from disk..')
        return torch.load(self.filename)
    node_ids = np.arange(num_nodes)
    node_list = [network.graph.nodes[idx] for idx in node_ids]
    print('Computing BERT embeddings..')
    self.bert_model.eval()
    eval_examples = convert_nodes_to_examples(node_list)
    eval_features = convert_examples_to_features(eval_examples, max_seq_length=self.max_seq_length, tokenizer=self.tokenizer)
    all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)
    eval_sampler = SequentialSampler(eval_data)
    eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=self.eval_batch_size)
    sequence_outputs = []
    for (input_ids, input_mask, segment_ids) in eval_dataloader:
        input_ids = input_ids.to(self.device)
        input_mask = input_mask.to(self.device)
        segment_ids = segment_ids.to(self.device)
        with torch.no_grad():
            (sequence_output, _) = self.bert_model.bert(input_ids, segment_ids, input_mask, output_all_encoded_layers=False)
        sequence_outputs.append(sequence_output[(:, 0)])
    return torch.cat(sequence_outputs, dim=0)
