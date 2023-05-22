from tqdm import tqdm
from utils.utils import AverageMeter, compute_reps, channelwise_clamp, get_softmax_probs
import torch
import torch.nn as nn
import torch.nn.functional as F


def attack_instances_consistency(model, images, labels, orig_preds, eps, alpha, distrib_params, criterion, iterations=50, rand=False, magnet_data=None, kl_loss=False):

    def get_rand_perturb(images, eps):
        pert = torch.rand_like(images)
        pert = (((2 * eps) * pert) - eps)
        return pert
    if kl_loss:
        iterations = 10
        alpha[(alpha > 0)] = 0.03
        criterion = torch.nn.KLDivLoss(size_average=False)
    assert (magnet_data is not None)
    device = images.device
    alphas = alpha.unsqueeze(2).unsqueeze(3).to(device)
    epss = eps.unsqueeze(0).unsqueeze(2).unsqueeze(3).to(device)
    (minima, maxima) = (distrib_params['minima'], distrib_params['maxima'])
    minima = minima.unsqueeze(0).unsqueeze(2).unsqueeze(3).to(device)
    maxima = maxima.unsqueeze(0).unsqueeze(2).unsqueeze(3).to(device)
    if rand:
        perturbed_images = (images.data + get_rand_perturb(images, epss))
        perturbed_images = channelwise_clamp(perturbed_images, minima=minima, maxima=maxima).data.clone()
    else:
        perturbed_images = images.data.clone()
    for _ in range(iterations):
        perturbed_images.requires_grad = True
        model.zero_grad()
        (_, embeddings) = model(perturbed_images)
        scores = get_softmax_probs(embeddings=embeddings, magnet_data=magnet_data, return_scores=True).to(device)
        if kl_loss:
            cost = criterion(F.log_softmax(scores, dim=1), labels)
        elif isinstance(criterion, nn.MSELoss):
            cost = criterion(labels, embeddings)
        else:
            cost = criterion(labels, scores)
        cost.backward()
        with torch.no_grad():
            eta = perturbed_images.grad.sign()
            perturbed_images += (alphas * eta)
            noise = (perturbed_images - images)
            noise = channelwise_clamp(noise, minima=(- epss), maxima=epss)
            perturbed_images = channelwise_clamp((images + noise), minima=minima, maxima=maxima)
    return perturbed_images
