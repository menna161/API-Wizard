import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions.categorical import Categorical
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import babyai.rl
from babyai.rl.utils.supervised_losses import required_heads


def _get_instr_embedding(self, instr):
    if (not self.enable_instr):
        instr = instr[(:, (instr.size()[1] - (4 * self.instr_sents)):)]
    if self.instr_only:
        assert self.enable_instr
        instr = instr[(:, :(instr.size()[1] - (4 * self.instr_sents)))]
    if self.random_shuffled:
        instr = instr[(:, torch.randperm(instr.size()[1]))]
    lengths = (instr != 0).sum(1).long()
    if (self.lang_model == 'gru'):
        if (self.arch == 'fusion'):
            assert (not self.instr_only)
            if self.enable_instr:
                desc = instr[(:, (instr.size()[1] - (4 * self.instr_sents)):)]
                ins = instr[(:, :(instr.size()[1] - (4 * self.instr_sents)))]
                lengths = (desc != 0).sum(1).long()
                lengths /= self.instr_sents
                hiddens = []
                for i in range(self.instr_sents):
                    (out, _) = self.instr_rnn(self.word_embedding(desc[(:, (4 * i):(4 * (i + 1)))]))
                    hidden = out[(range(len(lengths)), (lengths - 1), :)]
                    hiddens.append(hidden)
                hidden_desc = torch.stack(hiddens, axis=(- 1))
                lengths = (ins != 0).sum(1).long()
                (out, _) = self.instr_rnn(self.word_embedding(ins))
                hidden_instr = out[(range(len(lengths)), (lengths - 1), :)]
                return (hidden_desc, hidden_instr)
            else:
                lengths /= self.instr_sents
                hiddens = []
                for i in range(self.instr_sents):
                    (out, _) = self.instr_rnn(self.word_embedding(instr[(:, (4 * i):(4 * (i + 1)))]))
                    hidden = out[(range(len(lengths)), (lengths - 1), :)]
                    hiddens.append(hidden)
                hidden = torch.stack(hiddens, axis=(- 1))
        else:
            (out, _) = self.instr_rnn(self.word_embedding(instr))
            hidden = out[(range(len(lengths)), (lengths - 1), :)]
        return hidden
    elif (self.lang_model in ['bigru', 'attgru']):
        if (self.arch == 'fusion'):
            raise NotImplementedError('For early fusion model, only gru model is supported!')
        masks = (instr != 0).float()
        if (lengths.shape[0] > 1):
            (seq_lengths, perm_idx) = lengths.sort(0, descending=True)
            iperm_idx = torch.LongTensor(perm_idx.shape).fill_(0)
            if instr.is_cuda:
                iperm_idx = iperm_idx.cuda()
            for (i, v) in enumerate(perm_idx):
                iperm_idx[v.data] = i
            inputs = self.word_embedding(instr)
            inputs = inputs[perm_idx]
            inputs = pack_padded_sequence(inputs, seq_lengths.data.cpu().numpy(), batch_first=True)
            (outputs, final_states) = self.instr_rnn(inputs)
        else:
            instr = instr[(:, 0:lengths[0])]
            (outputs, final_states) = self.instr_rnn(self.word_embedding(instr))
            iperm_idx = None
        final_states = final_states.transpose(0, 1).contiguous()
        final_states = final_states.view(final_states.shape[0], (- 1))
        if (iperm_idx is not None):
            (outputs, _) = pad_packed_sequence(outputs, batch_first=True)
            outputs = outputs[iperm_idx]
            final_states = final_states[iperm_idx]
        if (outputs.shape[1] < masks.shape[1]):
            masks = masks[(:, :(outputs.shape[1] - masks.shape[1]))]
        return (outputs if (self.lang_model == 'attgru') else final_states)
    else:
        ValueError('Undefined instruction architecture: {}'.format(self.use_desc))
