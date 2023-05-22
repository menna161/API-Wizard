import numpy as np
import datetime
from collections import defaultdict
from argparse import Namespace
import json
import os
import copy
from shutil import copyfile
from pointcloud import translate_transform_to_new_center_of_rotation


def evaluate(cfg, val_idxs, all_pred_translations, all_pred_angles, all_gt_translations, all_gt_angles, all_pred_centers, all_gt_pc1centers, eval_dir=None, accept_inverted_angle=False, detailed_eval=False, avg_window=5, mean_time=0):
    new_all_pred_translations = translate_transform_to_new_center_of_rotation(all_pred_translations, all_pred_angles, all_pred_centers, all_gt_pc1centers)
    np.set_printoptions(precision=3, suppress=True)
    tracks = defaultdict(dict)
    empty_dict = {'corr_levels_translation': np.array([0, 0, 0], dtype=float), 'corr_levels_angles': np.array([0, 0, 0], dtype=float), 'corr_levels': np.array([0, 0, 0], dtype=float), 'mean_dist_translation': 0.0, 'mean_sq_dist_translation': 0.0, 'mean_dist_angle': 0.0, 'mean_sq_dist_angle': 0.0, 'num': 0}
    eval_measures = {'all': copy.deepcopy(empty_dict), '5m': copy.deepcopy(empty_dict), '10m': copy.deepcopy(empty_dict), '15m': copy.deepcopy(empty_dict), '20m': copy.deepcopy(empty_dict), 'val': {'all': copy.deepcopy(empty_dict), '5m': copy.deepcopy(empty_dict), '10m': copy.deepcopy(empty_dict), '15m': copy.deepcopy(empty_dict), '20m': copy.deepcopy(empty_dict)}, 'test': {'all': copy.deepcopy(empty_dict), '5m': copy.deepcopy(empty_dict), '10m': copy.deepcopy(empty_dict), '15m': copy.deepcopy(empty_dict), '20m': copy.deepcopy(empty_dict)}}
    per_transform_info = []
    for (idx, val_idx, translation, gt_translation, pred_angle, gt_angle, gt_pc1center) in zip([x for x in range(len(val_idxs))], val_idxs, new_all_pred_translations, all_gt_translations, all_pred_angles, all_gt_angles, all_gt_pc1centers):
        meta = json.load(open(f'{cfg.data.basepath}/meta/{str(val_idx).zfill(8)}.json', 'r'))
        if ('KITTI_tracklets' in cfg.data.basepath):
            is_test = (('trackids' in meta) and (meta['trackids'][0] in [2, 6, 7, 8, 10]))
        elif ('Synth' in cfg.data.basepath):
            is_test = (idx >= 1000)
        (dist_transl, levels_transl) = eval_translation(translation, gt_translation)
        (dist_angle, levels_angle) = eval_angle(pred_angle, gt_angle, accept_inverted_angle=accept_inverted_angle)
        levels = eval_transform(translation, gt_translation, pred_angle, gt_angle, accept_inverted_angle=accept_inverted_angle)
        for _set in ['both', 'val', 'test']:
            if (dist_transl > 10000):
                continue
            node = eval_measures
            if (_set in ['val', 'test']):
                node = eval_measures[_set]
                if ((_set == 'test') != is_test):
                    continue
            for key in ['all', '5m', '10m', '15m', '20m']:
                centroid_distance = np.linalg.norm(gt_pc1center)
                if ((key == '5m') and (centroid_distance > 5.0)):
                    continue
                if ((key == '10m') and (centroid_distance > 10.0)):
                    continue
                if ((key == '15m') and (centroid_distance > 15.0)):
                    continue
                if ((key == '20m') and (centroid_distance > 20.0)):
                    continue
                node[key]['num'] += 1
                node[key]['corr_levels_translation'] += levels_transl
                node[key]['mean_dist_translation'] += dist_transl
                node[key]['mean_sq_dist_translation'] += (dist_transl * dist_transl)
                node[key]['corr_levels_angles'] += levels_angle
                node[key]['mean_dist_angle'] += dist_angle
                node[key]['mean_sq_dist_angle'] += (dist_angle * dist_angle)
                node[key]['corr_levels'] += levels
        if detailed_eval:
            per_transform_info.append([levels, dist_transl, dist_angle])
    for _set in ['both', 'val', 'test']:
        node = eval_measures
        if (_set in ['val', 'test']):
            node = eval_measures[_set]
        for key in ['all', '5m', '10m', '15m', '20m']:
            num_predictions = float(node[key]['num'])
            if (node[key]['num'] == 0):
                num_predictions = 1e-20
            node[key]['corr_levels_translation'] /= num_predictions
            node[key]['mean_dist_translation'] /= num_predictions
            node[key]['mean_sq_dist_translation'] = np.sqrt((node[key]['mean_sq_dist_translation'] / num_predictions))
            node[key]['corr_levels_angles'] /= num_predictions
            node[key]['mean_dist_angle'] /= num_predictions
            node[key]['mean_sq_dist_angle'] = np.sqrt((node[key]['mean_sq_dist_angle'] / num_predictions))
            node[key]['corr_levels'] /= num_predictions
    reg_eval_measures = np.array([0, 0], dtype=float)
    for (idx, file_idx) in enumerate(val_idxs):
        meta = json.load(open(f'{cfg.data.basepath}/meta/{str(file_idx).zfill(8)}.json', 'r'))
        if ('seq' in meta):
            seq = meta['seq']
            trackid = meta['trackids'][0]
            (frame1, frame2) = meta['frames']
            intermediate_trackid = ((seq * 10000000) + (trackid * 10000))
            pred_translation = all_pred_translations[idx]
            time_passed = 0.1
            tracks[intermediate_trackid][frame2] = (pred_translation, time_passed)
    if (len(tracks) > 0):
        velocities = process_velocities(tracks, eval_dir, avg_window)
        velocities
    eval_dict = Namespace(corr_levels=eval_measures['all']['corr_levels'].tolist(), corr_levels_translation=eval_measures['all']['corr_levels_translation'].tolist(), mean_dist_translation=eval_measures['all']['mean_dist_translation'], mean_sq_dist_translation=eval_measures['all']['mean_sq_dist_translation'], corr_levels_angles=eval_measures['all']['corr_levels_angles'].tolist(), mean_dist_angle=eval_measures['all']['mean_dist_angle'], mean_sq_dist_angle=eval_measures['all']['mean_sq_dist_angle'], num=eval_measures['all']['num'], eval_5m=get_at_dist_measures(eval_measures, '5m'), eval_10m=get_at_dist_measures(eval_measures, '10m'), eval_15m=get_at_dist_measures(eval_measures, '15m'), eval_20m=get_at_dist_measures(eval_measures, '20m'), val=Namespace(corr_levels=eval_measures['val']['all']['corr_levels'].tolist(), corr_levels_translation=eval_measures['val']['all']['corr_levels_translation'].tolist(), mean_dist_translation=eval_measures['val']['all']['mean_dist_translation'], mean_sq_dist_translation=eval_measures['val']['all']['mean_sq_dist_translation'], corr_levels_angles=eval_measures['val']['all']['corr_levels_angles'].tolist(), mean_dist_angle=eval_measures['val']['all']['mean_dist_angle'], mean_sq_dist_angle=eval_measures['val']['all']['mean_sq_dist_angle'], num=eval_measures['val']['all']['num'], eval_5m=get_at_dist_measures(eval_measures['val'], '5m'), eval_10m=get_at_dist_measures(eval_measures['val'], '10m'), eval_15m=get_at_dist_measures(eval_measures['val'], '15m'), eval_20m=get_at_dist_measures(eval_measures['val'], '20m')), test=Namespace(corr_levels=eval_measures['test']['all']['corr_levels'].tolist(), corr_levels_translation=eval_measures['test']['all']['corr_levels_translation'].tolist(), mean_dist_translation=eval_measures['test']['all']['mean_dist_translation'], mean_sq_dist_translation=eval_measures['test']['all']['mean_sq_dist_translation'], corr_levels_angles=eval_measures['test']['all']['corr_levels_angles'].tolist(), mean_dist_angle=eval_measures['test']['all']['mean_dist_angle'], mean_sq_dist_angle=eval_measures['test']['all']['mean_sq_dist_angle'], num=eval_measures['test']['all']['num'], eval_5m=get_at_dist_measures(eval_measures['test'], '5m'), eval_10m=get_at_dist_measures(eval_measures['test'], '10m'), eval_15m=get_at_dist_measures(eval_measures['test'], '15m'), eval_20m=get_at_dist_measures(eval_measures['test'], '20m')), reg_eval=Namespace(fitness=reg_eval_measures[0], inlier_rmse=reg_eval_measures[1]), mean_time=mean_time)
    if (eval_dir is not None):
        os.makedirs(eval_dir, exist_ok=True)
        filename = f"{eval_dir}/eval{('_180' if accept_inverted_angle else '')}.json"
        if os.path.isfile(filename):
            datestr_now = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            copyfile(filename, f'{filename[:(- 5)]}_{datestr_now}.json')
            if (mean_time == 0):
                prev_eval_dict = json.load(open(filename, 'r'))
                if ('mean_time' in prev_eval_dict):
                    eval_dict.__dict__['mean_time'] = prev_eval_dict['mean_time']
        with open(filename, 'w') as fhandle:
            json.dump(ns_to_dict(eval_dict), fhandle)
    if detailed_eval:
        return (eval_dict, per_transform_info)
    return eval_dict
