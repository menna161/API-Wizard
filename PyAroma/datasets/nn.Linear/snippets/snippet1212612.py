import torch
import torch.nn as nn


def __init__(self, embeddings_size, decoder_size, attention_size, output_size):
    super(ContextGate, self).__init__()
    input_size = ((embeddings_size + decoder_size) + attention_size)
    self.gate = nn.Linear(input_size, output_size, bias=True)
    self.sig = nn.Sigmoid()
    self.source_proj = nn.Linear(attention_size, output_size)
    self.target_proj = nn.Linear((embeddings_size + decoder_size), output_size)
