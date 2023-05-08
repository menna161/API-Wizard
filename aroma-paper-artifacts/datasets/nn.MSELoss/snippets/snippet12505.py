from vocoder.models.fatchord_version import WaveRNN
from vocoder.vocoder_dataset import VocoderDataset, collate_vocoder
from vocoder.distribution import discretized_mix_logistic_loss
from vocoder.display import stream, simple_table
from vocoder.gen_wavernn import gen_testset
from torch.utils.data import DataLoader
from pathlib import Path
from torch import optim
import torch.nn.functional as F
import vocoder.hparams as hp
import numpy as np
import time
from vocoder.model_vc import *
import torch.nn as nn
from vocoder.griffin_lin import *
import scipy
import matplotlib.pyplot as plt
import torch
from synthesizer import audio
from synthesizer.hparams import hparams


def train(run_id: str, syn_dir: Path, voc_dir: Path, models_dir: Path, ground_truth: bool, save_every: int, backup_every: int, force_restart: bool):
    print('Initializing the model...')
    model = model_VC(32, 256, 512, 32).cuda()
    optimizer = optim.Adam(model.parameters())
    for p in optimizer.param_groups:
        p['lr'] = hp.voc_lr
    loss_recon = nn.MSELoss()
    loss_content = nn.L1Loss()
    model_dir = models_dir.joinpath(run_id)
    model_dir.mkdir(exist_ok=True)
    weights_fpath = model_dir.joinpath((run_id + '.pt'))
    if (force_restart or (not weights_fpath.exists())):
        print('\nStarting the training of AutoVC from scratch\n')
        model.save(weights_fpath, optimizer)
    else:
        print(('\nLoading weights at %s' % weights_fpath))
        model.load(weights_fpath, optimizer)
        print(('AutoVC weights loaded from step %d' % model.step))
    metadata_fpath = (syn_dir.joinpath('train.txt') if ground_truth else voc_dir.joinpath('synthesized.txt'))
    mel_dir = (syn_dir.joinpath('mels') if ground_truth else voc_dir.joinpath('mels_gta'))
    wav_dir = syn_dir.joinpath('audio')
    embed_dir = syn_dir.joinpath('embeds')
    dataset = VocoderDataset(metadata_fpath, mel_dir, wav_dir, embed_dir)
    test_loader = DataLoader(dataset, batch_size=1, shuffle=True, pin_memory=True)
    simple_table([('Batch size', hp.voc_batch_size), ('LR', hp.voc_lr), ('Sequence Len', hp.voc_seq_len)])
    for epoch in range(1, 350):
        model.train()
        data_loader = DataLoader(dataset, collate_fn=collate_vocoder, batch_size=hp.voc_batch_size, num_workers=2, shuffle=True, pin_memory=True)
        start = time.time()
        running_loss = 0.0
        for (i, (m, e, _)) in enumerate(data_loader, 1):
            model.train()
            (m, e) = (m.cuda(), e.cuda())
            (C, X_C, X_before, X_after, _) = model(m, e, e)
            X_after = X_after.squeeze(1).permute(0, 2, 1)
            X_before = X_before.squeeze(1).permute(0, 2, 1)
            loss_rec_before = loss_recon(X_before, m)
            loss_rec_after = loss_recon(X_after, m)
            loss_c = loss_content(C, X_C)
            loss = ((loss_rec_before + loss_rec_after) + loss_c)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            speed = (i / (time.time() - start))
            avg_loss = (running_loss / i)
            step = model.get_step()
            if (hp.decay_learning_rate == True):
                p['lr'] = _learning_rate_decay(p['lr'], step)
            k = (step // 1000)
            if (((step % 100) == 0) and (step != 0)):
                model.eval()
                plt.figure(1)
                (C, X_C, X_before, X_after, _) = model(m, e, e)
                X_after = X_after.squeeze(1).permute(0, 2, 1)
                mel_out = torch.tensor(X_after).clone().detach().cpu().numpy()
                from synthesizer import audio
                from synthesizer.hparams import hparams
                wav = audio.inv_mel_spectrogram(mel_out[(0, :, :)], hparams)
                librosa.output.write_wav('out.wav', np.float32(wav), hparams.sample_rate)
                mel_out = mel_out[(0, :, :)].transpose(1, 0)
                plt.imshow(mel_out.T, interpolation='nearest', aspect='auto')
                plt.title('Generate Spectrogram')
                save_path = model_dir
                p_path = save_path.joinpath('generate.png')
                plt.savefig(p_path)
                plt.figure(2)
                m_out = m.squeeze(1).permute(0, 2, 1)
                m_out = torch.tensor(m).clone().detach().cpu().numpy()
                m_out = m_out[(0, :, :)].transpose(1, 0)
                plt.imshow(m_out.T, interpolation='nearest', aspect='auto')
                plt.title('Orignal Spectrogram')
                o_path = save_path.joinpath('orignal.png')
                plt.savefig(o_path)
            if ((backup_every != 0) and ((step % backup_every) == 0)):
                model.checkpoint(model_dir, optimizer)
            if ((save_every != 0) and ((step % save_every) == 0)):
                model.save(weights_fpath, optimizer)
                torch.save(model, 'model_ttsdb_48_48.pkl')
            msg = f'| Epoch: {epoch} ({i}/{len(data_loader)}) | Loss: {avg_loss:.4f} | {speed:.1f} steps/s | Step: {k}k | '
            stream(msg)
        print('')
