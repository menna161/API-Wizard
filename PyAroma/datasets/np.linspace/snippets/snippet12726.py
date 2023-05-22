import torch
import torch.nn as nn
import torch.nn.functional as F
from vocoder.distribution import sample_from_discretized_mix_logistic
from vocoder.display import *
from vocoder.audio import *


def generate(self, mels, batched, target, overlap, mu_law, progress_callback=None):
    mu_law = (mu_law if (self.mode == 'RAW') else False)
    progress_callback = (progress_callback or self.gen_display)
    self.eval()
    output = []
    start = time.time()
    rnn1 = self.get_gru_cell(self.rnn1)
    rnn2 = self.get_gru_cell(self.rnn2)
    with torch.no_grad():
        mels = mels.cuda()
        wave_len = ((mels.size((- 1)) - 1) * self.hop_length)
        mels = self.pad_tensor(mels.transpose(1, 2), pad=self.pad, side='both')
        (mels, aux) = self.upsample(mels.transpose(1, 2))
        if batched:
            mels = self.fold_with_overlap(mels, target, overlap)
            aux = self.fold_with_overlap(aux, target, overlap)
        (b_size, seq_len, _) = mels.size()
        h1 = torch.zeros(b_size, self.rnn_dims).cuda()
        h2 = torch.zeros(b_size, self.rnn_dims).cuda()
        x = torch.zeros(b_size, 1).cuda()
        d = self.aux_dims
        aux_split = [aux[(:, :, (d * i):(d * (i + 1)))] for i in range(4)]
        for i in range(seq_len):
            m_t = mels[(:, i, :)]
            (a1_t, a2_t, a3_t, a4_t) = (a[(:, i, :)] for a in aux_split)
            x = torch.cat([x, m_t, a1_t], dim=1)
            x = self.I(x)
            h1 = rnn1(x, h1)
            x = (x + h1)
            inp = torch.cat([x, a2_t], dim=1)
            h2 = rnn2(inp, h2)
            x = (x + h2)
            x = torch.cat([x, a3_t], dim=1)
            x = F.relu(self.fc1(x))
            x = torch.cat([x, a4_t], dim=1)
            x = F.relu(self.fc2(x))
            logits = self.fc3(x)
            if (self.mode == 'MOL'):
                sample = sample_from_discretized_mix_logistic(logits.unsqueeze(0).transpose(1, 2))
                output.append(sample.view((- 1)))
                x = sample.transpose(0, 1).cuda()
            elif (self.mode == 'RAW'):
                posterior = F.softmax(logits, dim=1)
                distrib = torch.distributions.Categorical(posterior)
                sample = (((2 * distrib.sample().float()) / (self.n_classes - 1.0)) - 1.0)
                output.append(sample)
                x = sample.unsqueeze((- 1))
            else:
                raise RuntimeError('Unknown model mode value - ', self.mode)
            if ((i % 100) == 0):
                gen_rate = ((((i + 1) / (time.time() - start)) * b_size) / 1000)
                progress_callback(i, seq_len, b_size, gen_rate)
    output = torch.stack(output).transpose(0, 1)
    output = output.cpu().numpy()
    output = output.astype(np.float64)
    if batched:
        output = self.xfade_and_unfold(output, target, overlap)
    else:
        output = output[0]
    if mu_law:
        output = decode_mu_law(output, self.n_classes, False)
    if hp.apply_preemphasis:
        output = de_emphasis(output)
    fade_out = np.linspace(1, 0, (20 * self.hop_length))
    output = output[:wave_len]
    output[((- 20) * self.hop_length):] *= fade_out
    self.train()
    return output
