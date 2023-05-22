import torch
from torch.autograd import Variable


def __init__(self, vocab_size, emb_dim, share_emb_weight=True):
    '\n        embedding and decoding.\n        '
    super().__init__()
    self.embedding = torch.nn.Embedding(vocab_size, emb_dim)
    torch.nn.init.uniform_(self.embedding.weight, (- 1.0), 1.0)
    '\n        For embedding weight sharing.\n        '
    if share_emb_weight:
        self.proj2vocab = torch.nn.Linear(emb_dim, vocab_size)
        self.proj2vocab.weight.data = self.embedding.weight.data
