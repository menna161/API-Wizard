import os, sys, numpy, torch, argparse, skimage, json, shutil
from PIL import Image
from torch.utils.data import TensorDataset
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.gridspec as gridspec
from scipy.ndimage.morphology import binary_dilation
import netdissect.zdataset
import netdissect.nethook
from netdissect.dissection import safe_dir_name
from netdissect.progress import verbose_progress, default_progress
from netdissect.progress import print_progress, desc_progress, post_progress
from netdissect.easydict import EasyDict
from netdissect.workerpool import WorkerPool, WorkerBase
from netdissect.runningstats import RunningQuantile
from netdissect.pidfile import pidfile_taken
from netdissect.modelconfig import create_instrumented_model
from netdissect.autoeval import autoimport_eval


def train_ablation(args, corpus, cachefile, model, segmenter, classnum, initial_ablation=None):
    progress = default_progress()
    cachedir = os.path.dirname(cachefile)
    snapdir = os.path.join(cachedir, 'snapshots')
    os.makedirs(snapdir, exist_ok=True)
    if ('_h99' in args.variant):
        high_replacement = corpus.feature_99[(None, :, None, None)].cuda()
    elif ('_tcm' in args.variant):
        high_replacement = corpus.mean_present_feature[(None, :, None, None)].cuda()
    else:
        high_replacement = corpus.weighted_mean_present_feature[(None, :, None, None)].cuda()
    fullimage_measurement = False
    ablation_only = False
    fullimage_ablation = False
    if ('_fim' in args.variant):
        fullimage_measurement = True
    elif ('_fia' in args.variant):
        fullimage_measurement = True
        ablation_only = True
        fullimage_ablation = True
    high_replacement.requires_grad = False
    for p in model.parameters():
        p.requires_grad = False
    ablation = torch.zeros(high_replacement.shape).cuda()
    if (initial_ablation is not None):
        ablation.view((- 1))[...] = initial_ablation
    ablation.requires_grad = True
    optimizer = torch.optim.Adam([ablation], lr=0.01)
    start_epoch = 0
    epoch = 0

    def eval_loss_and_reg():
        discrete_experiments = dict(dboth20=dict(discrete_units=20, discrete_pixels=True), fimadbm10=dict(discrete_units=10, mixed_units=True, discrete_pixels=True, ablation_only=True, fullimage_ablation=True, fullimage_measurement=True), fimadbm20=dict(discrete_units=20, mixed_units=True, discrete_pixels=True, ablation_only=True, fullimage_ablation=True, fullimage_measurement=True))
        with torch.no_grad():
            total_loss = 0
            discrete_losses = {k: 0 for k in discrete_experiments}
            for [pbatch, ploc, cbatch, cloc] in progress(torch.utils.data.DataLoader(TensorDataset(corpus.eval_present_sample, corpus.eval_present_location, corpus.eval_candidate_sample, corpus.eval_candidate_location), batch_size=args.inference_batch_size, num_workers=10, shuffle=False, pin_memory=True), desc='Eval'):
                total_loss = (total_loss + ace_loss(segmenter, classnum, model, args.layer, high_replacement, ablation, pbatch, ploc, cbatch, cloc, run_backward=False, ablation_only=ablation_only, fullimage_measurement=fullimage_measurement))
                for (k, config) in discrete_experiments.items():
                    discrete_losses[k] = (discrete_losses[k] + ace_loss(segmenter, classnum, model, args.layer, high_replacement, ablation, pbatch, ploc, cbatch, cloc, run_backward=False, **config))
            avg_loss = (total_loss / args.eval_size).item()
            avg_d_losses = {k: (d / args.eval_size).item() for (k, d) in discrete_losses.items()}
            regularizer = (args.l2_lambda * ablation.pow(2).sum())
            print_progress(('Epoch %d Loss %g Regularizer %g' % (epoch, avg_loss, regularizer)))
            print_progress(' '.join((('%s: %g' % (k, d)) for (k, d) in avg_d_losses.items())))
            print_progress(scale_summary(ablation.view((- 1)), 10, 3))
            return (avg_loss, regularizer, avg_d_losses)
    if args.eval_only:
        for epoch in range((- 1), args.train_epochs):
            snapfile = os.path.join(snapdir, ('epoch-%d.pth' % epoch))
            if (not os.path.exists(snapfile)):
                data = {}
                if (epoch >= 0):
                    print(('No epoch %d' % epoch))
                    continue
            else:
                data = torch.load(snapfile)
                with torch.no_grad():
                    ablation[...] = data['ablation'].to(ablation.device)
                    optimizer.load_state_dict(data['optimizer'])
            (avg_loss, regularizer, new_extra) = eval_loss_and_reg()
            extra = {k: v for (k, v) in data.items() if (k not in ['ablation', 'optimizer', 'avg_loss'])}
            extra.update(new_extra)
            torch.save(dict(ablation=ablation, optimizer=optimizer.state_dict(), avg_loss=avg_loss, **extra), os.path.join(snapdir, ('epoch-%d.pth' % epoch)))
        return ablation.view((- 1)).detach().cpu().numpy()
    if (not args.no_cache):
        for start_epoch in reversed(range(args.train_epochs)):
            snapfile = os.path.join(snapdir, ('epoch-%d.pth' % start_epoch))
            if os.path.exists(snapfile):
                data = torch.load(snapfile)
                with torch.no_grad():
                    ablation[...] = data['ablation'].to(ablation.device)
                    optimizer.load_state_dict(data['optimizer'])
                start_epoch += 1
                break
    if (start_epoch < args.train_epochs):
        epoch = (start_epoch - 1)
        (avg_loss, regularizer, extra) = eval_loss_and_reg()
        if (epoch == (- 1)):
            torch.save(dict(ablation=ablation, optimizer=optimizer.state_dict(), avg_loss=avg_loss, **extra), os.path.join(snapdir, ('epoch-%d.pth' % epoch)))
    update_size = (args.train_update_freq * args.train_batch_size)
    for epoch in range(start_epoch, args.train_epochs):
        candidate_shuffle = torch.randperm(len(corpus.candidate_sample))
        train_loss = 0
        for (batch_num, [pbatch, ploc, cbatch, cloc]) in enumerate(progress(torch.utils.data.DataLoader(TensorDataset(corpus.object_present_sample, corpus.object_present_location, corpus.candidate_sample[candidate_shuffle], corpus.candidate_location[candidate_shuffle]), batch_size=args.train_batch_size, num_workers=10, shuffle=True, pin_memory=True), desc=('ACE opt epoch %d' % epoch))):
            if ((batch_num % args.train_update_freq) == 0):
                optimizer.zero_grad()
            loss = ace_loss(segmenter, classnum, model, args.layer, high_replacement, ablation, pbatch, ploc, cbatch, cloc, run_backward=True, ablation_only=ablation_only, fullimage_measurement=fullimage_measurement)
            with torch.no_grad():
                train_loss = (train_loss + loss)
            if (((batch_num + 1) % args.train_update_freq) == 0):
                regularizer = ((args.l2_lambda * update_size) * ablation.pow(2).sum())
                regularizer.backward()
                optimizer.step()
                with torch.no_grad():
                    ablation.clamp_(0, 1)
                    post_progress(l=(train_loss / update_size).item(), r=(regularizer / update_size).item())
                    train_loss = 0
        (avg_loss, regularizer, extra) = eval_loss_and_reg()
        torch.save(dict(ablation=ablation, optimizer=optimizer.state_dict(), avg_loss=avg_loss, **extra), os.path.join(snapdir, ('epoch-%d.pth' % epoch)))
        numpy.save(os.path.join(snapdir, ('epoch-%d.npy' % epoch)), ablation.detach().cpu().numpy())
    return ablation.view((- 1)).detach().cpu().numpy()
