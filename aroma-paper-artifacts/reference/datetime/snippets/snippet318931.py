import torch
import argparse
import numpy as np
import utils
from pathlib import Path
from datetime import datetime
from network import ContactsNet
from dataset import ProteinDataLoader


def run_eval(target_path, model_path, replica, out_dir, device):
    config = utils.build_config(model_path, replica)
    dataloader = ProteinDataLoader(target_path, config)
    model = ContactsNet(config.network_config).to(device)
    print(f"Model parameters: {model.get_parameter_number()['Total']}")
    model_file = ((model_path / replica) / 'model.pt')
    if model_file.exists():
        model.load_state_dict(torch.load(model_file, map_location=device))
    else:
        cost_time = utils.load_tf_ckpt(model, model_file)
        model.to(device)
        print(f'Load tf model cost time: {cost_time}')
    num_examples = 0
    num_crops = 0
    num_bins = config.network_config.num_bins
    torsion_bins = config.network_config.torsion_bins
    crop_size_x = config.crop_size_x
    crop_size_y = config.crop_size_y
    prob_weights = 1
    if (config.eval_config.pyramid_weights > 0):
        sx = np.expand_dims(np.linspace((1.0 / crop_size_x), 1, crop_size_x), 1)
        sy = np.expand_dims(np.linspace((1.0 / crop_size_y), 1, crop_size_y), 0)
        prob_weights = np.minimum(np.minimum(sx, np.flipud(sx)), np.minimum(sy, np.fliplr(sy)))
        prob_weights /= np.max(prob_weights)
        prob_weights = np.minimum(prob_weights, config.eval_config.pyramid_weights)
    start_t = datetime.now()
    for (protein, crops) in dataloader:
        L = protein.len
        print('Data: ', protein.targets.domain_name, L)
        contact_prob_accum = np.zeros((L, L, 2), dtype=np.float32)
        distance_prob_accum = np.zeros((L, L, num_bins), dtype=np.float32)
        sec_accum = np.zeros((L, 8), dtype=np.float32)
        tor_accum = np.zeros((L, (torsion_bins ** 2)), dtype=np.float32)
        asa_accum = np.zeros((L,), dtype=np.float32)
        weights_1d_accum = np.zeros((L,), dtype=np.float32)
        num_crops_local = 0
        for (x_2d, crop_x, crop_y) in crops:
            ic = max(0, crop_x[0])
            jc = max(0, crop_y[0])
            ic_to = min(L, crop_x[1])
            jc_to = min(L, crop_y[1])
            prepad_x = max(0, (- crop_x[0]))
            prepad_y = max(0, (- crop_y[0]))
            postpad_x = (crop_x[1] - ic_to)
            postpad_y = (crop_y[1] - jc_to)
            with torch.no_grad():
                x_2d = np.transpose(x_2d, (2, 0, 1))
                x_2d = torch.tensor([x_2d]).float().to(device)
                crop_x = torch.tensor([crop_x]).to(device)
                crop_y = torch.tensor([crop_y]).to(device)
                out = model(x_2d, crop_x, crop_y)
                out = {k: t.cpu() for (k, t) in out.items()}
            contact_probs = out['contact_probs'][0, prepad_y:(crop_size_y - postpad_y), prepad_x:(crop_size_x - postpad_x)].numpy()
            distance_probs = out['distance_probs'][0, prepad_y:(crop_size_y - postpad_y), prepad_x:(crop_size_x - postpad_x)].numpy()
            weight = prob_weights[prepad_y:(crop_size_y - postpad_y), prepad_x:(crop_size_x - postpad_x)]
            contact_prob_accum[jc:jc_to, ic:ic_to, 0] += (contact_probs * weight)
            contact_prob_accum[jc:jc_to, ic:ic_to, 1] += weight
            distance_prob_accum[jc:jc_to, ic:ic_to, :] += (distance_probs * np.expand_dims(weight, 2))
            weights_1d_accum[jc:jc_to] += 1
            weights_1d_accum[ic:ic_to] += 1
            if ('secstruct_probs' in out):
                sec_x = out['secstruct_probs'][0, prepad_x:(crop_size_x - postpad_x)].numpy()
                sec_y = out['secstruct_probs'][0, (crop_size_x + prepad_y):((crop_size_x + crop_size_y) - postpad_y)].numpy()
                sec_accum[ic:(ic + sec_x.shape[0])] += sec_x
                sec_accum[jc:(jc + sec_y.shape[0])] += sec_y
            if ('torsion_probs' in out):
                tor_x = out['torsion_probs'][0, prepad_x:(crop_size_x - postpad_x)].numpy()
                tor_y = out['torsion_probs'][0, (crop_size_x + prepad_y):((crop_size_x + crop_size_y) - postpad_y)].numpy()
                tor_accum[ic:(ic + tor_x.shape[0])] += tor_x
                tor_accum[jc:(jc + tor_y.shape[0])] += tor_y
            if ('asa_output' in out):
                asa_x = out['asa_output'][0, prepad_x:(crop_size_x - postpad_x)].numpy()
                asa_y = out['asa_output'][0, (crop_size_x + prepad_y):((crop_size_x + crop_size_y) - postpad_y)].numpy()
                asa_accum[ic:(ic + asa_x.shape[0])] += np.squeeze(asa_x, 1)
                asa_accum[jc:(jc + asa_y.shape[0])] += np.squeeze(asa_y, 1)
            num_crops_local += 1
        assert (contact_prob_accum[:, :, 1] > 0.0).all()
        contact_accum = (contact_prob_accum[:, :, 0] / contact_prob_accum[:, :, 1])
        distance_accum = (distance_prob_accum[:, :, :] / contact_prob_accum[:, :, 1:2])
        asa_accum /= weights_1d_accum
        sec_accum /= np.expand_dims(weights_1d_accum, 1)
        tor_accum /= np.expand_dims(weights_1d_accum, 1)
        contact_accum = ((contact_accum + contact_accum.transpose()) / 2)
        distance_accum = ((distance_accum + np.transpose(distance_accum, [1, 0, 2])) / 2)
        distance_accum.dump((out_dir / f'{protein.targets.domain_name}.distance'))
        if (config.network_config.torsion_multiplier > 0):
            tor_accum.dump((out_dir / f'{protein.targets.domain_name}.torsion'))
        if (config.network_config.secstruct_multiplier > 0):
            utils.save_seq_prob(sec_accum, protein.seq, (out_dir / f'{protein.targets.domain_name}.sec'))
        if (config.network_config.asa_multiplier > 0):
            utils.save_seq_prob(asa_accum, protein.seq, (out_dir / f'{protein.targets.domain_name}.asa'))
        num_examples += 1
        num_crops += num_crops_local
        if (num_examples >= config.eval_config.max_num_examples):
            break
    time_spent = (datetime.now() - start_t)
    print(f'Evaluate {num_examples} examples, {num_crops} crops, {(num_crops / num_examples):.1f} crops/ex')
    print(f'''Cost time {time_spent}, {(time_spent / num_examples)} s/example, {(time_spent / num_crops)} s/crops
''')
