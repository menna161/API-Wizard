from tqdm import tqdm
from utils.utils import AverageMeter, compute_reps, channelwise_clamp, get_softmax_probs
import torch
import torch.nn as nn
import torch.nn.functional as F


def run_magnet_epoch(model, optimizer, trainloader, device, trainset, train_labels, batch_builder, print_freq, cluster_refresh_interval, criterion, eps, magnet_data, distrib_params, alpha=(10 / 255), actual_trades=False):
    consist_crit = (nn.MSELoss() if magnet_data['mse_consistency'] else cross_ent)
    model.train()
    losses = AverageMeter()
    pbar = tqdm(range(len(trainloader)))
    for iteration in pbar:
        (batch_inds, class_inds, clust_assigns) = batch_builder.gen_batch()
        trainloader.sampler.batch_indices = batch_inds
        for (img, target) in trainloader:
            (img, target) = (img.to(device), target.to(device))
            optimizer.zero_grad()
            (_, embs) = model(img)
            (loss, inst_losses, _) = criterion(embs, class_inds, clust_assigns)
            if (magnet_data['consistency_lambda'] > 0.0):
                probs = get_softmax_probs(embeddings=embs, magnet_data=magnet_data).to(device)
                (_, orig_preds) = torch.max(probs.data, 1)
                eps_p = (eps / distrib_params['std'])
                alpha_p = (alpha / distrib_params['std'].unsqueeze(0))
                p_labels = (embs if magnet_data['mse_consistency'] else probs)
                adv_instances = attack_instances_consistency(model, images=img, labels=p_labels.detach(), orig_preds=orig_preds, eps=eps_p, distrib_params=distrib_params, alpha=alpha_p, criterion=consist_crit, magnet_data=magnet_data, iterations=1, rand=True, kl_loss=actual_trades)
                (_, adv_embs) = model(adv_instances)
                if magnet_data['mse_consistency']:
                    consistency_loss = consist_crit(adv_embs, embs)
                else:
                    adv_scores = get_softmax_probs(embeddings=adv_embs, magnet_data=magnet_data, return_scores=True)
                    consistency_loss = consist_crit(probs, adv_scores)
                loss = (loss + (magnet_data['consistency_lambda'] * consistency_loss))
            if (magnet_data['xent_lambda'] > 0.0):
                xent_crit = nn.CrossEntropyLoss()
                class_scores = get_softmax_probs(embeddings=embs, magnet_data=magnet_data, return_scores=True).to(device)
                xent_loss = xent_crit(class_scores, target)
                loss = (loss + (magnet_data['xent_lambda'] * xent_loss))
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                batch_builder.update_losses(batch_inds, inst_losses)
            losses.update(loss.item(), img.size(0))
            if ((iteration % print_freq) == 0):
                pbar.set_description(f'Loss: {losses.avg:4.3f}')
            if (((iteration % cluster_refresh_interval) == 0) and (iteration != 0)):
                model.eval()
                (_, reps) = compute_reps(model, trainset, 400)
                batch_builder.update_clusters(reps)
                model.train()
    return (model, batch_builder, losses)
