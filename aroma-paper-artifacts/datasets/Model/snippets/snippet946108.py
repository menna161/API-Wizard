import logging
import os
import sys
from typing import Dict, List, Optional
import torch
from fairseq.models import FairseqIncrementalDecoder, FairseqLanguageModel, register_model, register_model_architecture
from transformers import AutoModel, GPT2Config, GPT2LMHeadModel
from transformers import GPT2Config, GPT2LMHeadModel


def __init__(self, args, task):
    super().__init__(task.target_dictionary)
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'transformers', 'src'))
        from transformers import GPT2Config, GPT2LMHeadModel
    except ImportError:
        raise ImportError('\n\nPlease install huggingface/transformers with:\n\n  pip install transformers\n\nOr to make local edits, install the submodule:\n\n  git submodule update --init fairseq/models/huggingface/transformers')
    config = GPT2Config(vocab_size=len(task.target_dictionary), n_positions=(args.max_target_positions + 1), n_ctx=args.max_target_positions, n_embd=args.embed_dim, n_layer=args.num_layers, n_head=args.num_attention_heads, resid_pdrop=args.dropout, embd_pdrop=args.dropout, attn_pdrop=args.attention_dropout, layer_norm_epsilon=1e-06)
    self.model = GPT2LMHeadModel(config)
    self.pad_idx = task.target_dictionary.pad()
    self.model.transformer.wte.weight.data[self.pad_idx].zero_()
    self.model.transformer.wpe.weight.data[0].zero_()
