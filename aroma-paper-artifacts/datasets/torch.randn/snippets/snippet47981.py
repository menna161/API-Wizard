import math
import torch
import numpy as np
import torch.nn as nn


def sample_per_class_zs(model, num_classes, num, device, use_new_z_bound, z_mean_bound):
    "\n    Convenience method to draw samples from the prior and directly attach a label to them from the classifier.\n    In generative replay with outlier rejection, the samples' outlier probabilities can then be directly computed and\n    samples rejected or accepted before calculating the probabilistic decoder.\n\n    We have added an optional flag and optional specification of Gaussian prior standard deviation, even though it is\n    not described and has not been used in the original paper. The general idea is that if the optimization doesn't\n    succeed and the approximate posterior is far away from a unit Gaussian, during generative replay we can gauge\n    whether specific class regions of high density are sampled or not (as fitted by the Weibull models). If areas\n    of large class density lie outside the range of a Unit Gaussian, we can adaptively change the prior because we have\n    additional knowledge from the Weibull models on the expected range.\n\n    Parameters:\n        model (torch.nn.module): Trained model.\n        num_classes (int): Number of classes.\n        num (int): Number of samples to draw.\n        device (str): Device to compute on.\n        use_new_z_bound (bool): Flag indicating whether a modifed prior with larger std should be used.\n        z_mean_bound (float): New standard deviation for the Gaussian prior if use_new_z_bound is True.\n    "
    z_samples_per_class = []
    for i in range(num_classes):
        z_samples_per_class.append([])
    if use_new_z_bound:
        z_samples = (torch.randn(num, model.module.latent_dim).to(device) * z_mean_bound)
    else:
        z_samples = torch.randn(num, model.module.latent_dim).to(device)
    cl = model.module.classifier(z_samples)
    out = torch.nn.functional.softmax(cl, dim=1)
    for i in range(out.size(0)):
        idx = torch.argmax(out[i]).item()
        z_samples_per_class[idx].append(z_samples[i].data)
    for i in range(len(z_samples_per_class)):
        if (len(z_samples_per_class[i]) > 0):
            z_samples_per_class[i] = torch.stack(z_samples_per_class[i], dim=0)
    return {'z_samples': z_samples_per_class}
