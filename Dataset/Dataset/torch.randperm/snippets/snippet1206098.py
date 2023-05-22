import torch
import torch.nn.functional as F
import utils


def simba_batch(self, images_batch, labels_batch, max_iters, freq_dims, stride, epsilon, linf_bound=0.0, order='rand', targeted=False, pixel_attack=False, log_every=1):
    batch_size = images_batch.size(0)
    image_size = images_batch.size(2)
    assert (self.image_size == image_size)
    if (order == 'rand'):
        indices = torch.randperm(((3 * freq_dims) * freq_dims))[:max_iters]
    elif (order == 'diag'):
        indices = utils.diagonal_order(image_size, 3)[:max_iters]
    elif (order == 'strided'):
        indices = utils.block_order(image_size, 3, initial_size=freq_dims, stride=stride)[:max_iters]
    else:
        indices = utils.block_order(image_size, 3)[:max_iters]
    if (order == 'rand'):
        expand_dims = freq_dims
    else:
        expand_dims = image_size
    n_dims = ((3 * expand_dims) * expand_dims)
    x = torch.zeros(batch_size, n_dims)
    probs = torch.zeros(batch_size, max_iters)
    succs = torch.zeros(batch_size, max_iters)
    queries = torch.zeros(batch_size, max_iters)
    l2_norms = torch.zeros(batch_size, max_iters)
    linf_norms = torch.zeros(batch_size, max_iters)
    prev_probs = self.get_probs(images_batch, labels_batch)
    preds = self.get_preds(images_batch)
    if pixel_attack:
        trans = (lambda z: z)
    else:
        trans = (lambda z: utils.block_idct(z, block_size=image_size, linf_bound=linf_bound))
    remaining_indices = torch.arange(0, batch_size).long()
    for k in range(max_iters):
        dim = indices[k]
        expanded = (images_batch[remaining_indices] + trans(self.expand_vector(x[remaining_indices], expand_dims))).clamp(0, 1)
        perturbation = trans(self.expand_vector(x, expand_dims))
        l2_norms[(:, k)] = perturbation.view(batch_size, (- 1)).norm(2, 1)
        linf_norms[(:, k)] = perturbation.view(batch_size, (- 1)).abs().max(1)[0]
        preds_next = self.get_preds(expanded)
        preds[remaining_indices] = preds_next
        if targeted:
            remaining = preds.ne(labels_batch)
        else:
            remaining = preds.eq(labels_batch)
        if (remaining.sum() == 0):
            adv = (images_batch + trans(self.expand_vector(x, expand_dims))).clamp(0, 1)
            probs_k = self.get_probs(adv, labels_batch)
            probs[(:, k:)] = probs_k.unsqueeze(1).repeat(1, (max_iters - k))
            succs[(:, k:)] = torch.ones(batch_size, (max_iters - k))
            queries[(:, k:)] = torch.zeros(batch_size, (max_iters - k))
            break
        remaining_indices = torch.arange(0, batch_size)[remaining].long()
        if (k > 0):
            succs[(:, k)] = (~ remaining)
        diff = torch.zeros(remaining.sum(), n_dims)
        diff[(:, dim)] = epsilon
        left_vec = (x[remaining_indices] - diff)
        right_vec = (x[remaining_indices] + diff)
        adv = (images_batch[remaining_indices] + trans(self.expand_vector(left_vec, expand_dims))).clamp(0, 1)
        left_probs = self.get_probs(adv, labels_batch[remaining_indices])
        queries_k = torch.zeros(batch_size)
        queries_k[remaining_indices] += 1
        if targeted:
            improved = left_probs.gt(prev_probs[remaining_indices])
        else:
            improved = left_probs.lt(prev_probs[remaining_indices])
        if (improved.sum() < remaining_indices.size(0)):
            queries_k[remaining_indices[(~ improved)]] += 1
        adv = (images_batch[remaining_indices] + trans(self.expand_vector(right_vec, expand_dims))).clamp(0, 1)
        right_probs = self.get_probs(adv, labels_batch[remaining_indices])
        if targeted:
            right_improved = right_probs.gt(torch.max(prev_probs[remaining_indices], left_probs))
        else:
            right_improved = right_probs.lt(torch.min(prev_probs[remaining_indices], left_probs))
        probs_k = prev_probs.clone()
        if (improved.sum() > 0):
            left_indices = remaining_indices[improved]
            left_mask_remaining = improved.unsqueeze(1).repeat(1, n_dims)
            x[left_indices] = left_vec[left_mask_remaining].view((- 1), n_dims)
            probs_k[left_indices] = left_probs[improved]
        if (right_improved.sum() > 0):
            right_indices = remaining_indices[right_improved]
            right_mask_remaining = right_improved.unsqueeze(1).repeat(1, n_dims)
            x[right_indices] = right_vec[right_mask_remaining].view((- 1), n_dims)
            probs_k[right_indices] = right_probs[right_improved]
        probs[(:, k)] = probs_k
        queries[(:, k)] = queries_k
        prev_probs = probs[(:, k)]
        if ((((k + 1) % log_every) == 0) or (k == (max_iters - 1))):
            print(('Iteration %d: queries = %.4f, prob = %.4f, remaining = %.4f' % ((k + 1), queries.sum(1).mean(), probs[(:, k)].mean(), remaining.float().mean())))
    expanded = (images_batch + trans(self.expand_vector(x, expand_dims))).clamp(0, 1)
    preds = self.get_preds(expanded)
    if targeted:
        remaining = preds.ne(labels_batch)
    else:
        remaining = preds.eq(labels_batch)
    succs[(:, (max_iters - 1))] = (~ remaining)
    return (expanded, probs, succs, queries, l2_norms, linf_norms)
