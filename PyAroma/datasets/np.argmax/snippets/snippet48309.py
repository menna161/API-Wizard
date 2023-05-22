from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import pickle
import json
import numpy as np
import _init_paths
from opts import opts
from timer import Timer
from logger import Logger
from vsrl_eval import VCOCOeval
from apply_prior import apply_prior
from datasets.dataset_factory import dataset_factory
from detectors.detector_factory import detector_factory


def test(opt, Test_RCNN, prior_mask, Action_dic_inv, output_file, human_thres, object_thres, action_thres, detection):
    os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
    Dataset = dataset_factory[opt.dataset]
    opt = opts().update_dataset_info_and_set_heads(opt, Dataset)
    print(opt)
    Logger(opt)
    Detector = detector_factory[opt.task]
    detector = Detector(opt)
    dataset = Dataset(opt, 'test')
    num_iters = len(dataset)
    count = 0
    wo_object_list = [4, 18, 23, 28]
    total_list = [i for i in range(1, 30)]
    sigmoid_coeff = (6, 6, 7, 0)
    h_dis_thresh = 10
    ho_dis_thresh = 80
    _t = {'im_detect': Timer(), 'misc': Timer()}
    for ind in range(num_iters):
        _t['im_detect'].tic()
        img_id = dataset.images[ind]
        img_info = dataset.coco.loadImgs(ids=[img_id])[0]
        img_path = os.path.join('coco/images/trainval2017/', img_info['file_name'])
        ret = detector.run(img_path)
        for H_ins in Test_RCNN[img_id]:
            if ((np.max(H_ins[5]) > human_thres) and (H_ins[1] == 'Human')):
                h_box = H_ins[2]
                (h_c_x, h_c_y) = (((h_box[0] + h_box[2]) / 2), ((h_box[1] + h_box[3]) / 2))
                h_center = np.array([h_c_x, h_c_y])
                prediction_H = np.zeros(29)
                for i in wo_object_list:
                    if (len(ret[0][i]) != 0):
                        for a in ret[0][i]:
                            prediction_H[(i - 1)] = (a[6] if ((a[6] > action_thres) and (dis(a[0:2], h_center) < h_dis_thresh)) else 0)
                dic = {}
                dic['image_id'] = img_id
                dic['person_box'] = H_ins[2]
                h_score = getSigmoid(sigmoid_coeff, H_ins[5])
                Score_obj = np.empty((0, (4 + 29)), dtype=np.float32)
                for O_ins in Test_RCNN[img_id]:
                    if ((np.max(O_ins[5]) > object_thres) and (O_ins[1] == 'Object')):
                        o_box = O_ins[2]
                        prediction_HO = np.zeros(29)
                        o_score = getSigmoid(sigmoid_coeff, O_ins[5])
                        (o_c_x, o_c_y) = (((o_box[0] + o_box[2]) / 2), ((o_box[1] + o_box[3]) / 2))
                        for j in total_list:
                            if (j not in wo_object_list):
                                if (len(ret[0][j]) != 0):
                                    for a in ret[0][j]:
                                        iou_ao = iou(a[2:6], np.array(O_ins[2]))
                                        iou_ah = iou(a[2:6], np.array(H_ins[2]))
                                        if ((a[6] > action_thres) and (iou_ao > 0) and (iou_ah > 0)):
                                            ref_box = np.array([min(h_c_x, o_c_x), min(h_c_y, o_c_y), min(h_c_x, o_c_x), max(h_c_y, o_c_y), max(h_c_x, o_c_x), min(h_c_y, o_c_y), max(h_c_x, o_c_x), max(h_c_y, o_c_y)])
                                            inter_box = np.array([a[2], a[3], a[2], a[5], a[4], a[3], a[4], a[5]])
                                            dist_tl = dis(ref_box[0:2], inter_box[0:2])
                                            dist_tr = dis(ref_box[2:4], inter_box[2:4])
                                            dist_bl = dis(ref_box[4:6], inter_box[4:6])
                                            dist_br = dis(ref_box[6:8], inter_box[6:8])
                                            if ((dist_tl < ho_dis_thresh) and (dist_tr < ho_dis_thresh) and (dist_bl < ho_dis_thresh) and (dist_br < ho_dis_thresh)):
                                                prediction_HO[(j - 1)] = a[6]
                        prediction_HO = apply_prior(O_ins, prediction_HO)
                        prediction_HO = (prediction_HO * prior_mask[(:, O_ins[4])].reshape(1, 29))
                        This_Score_obj = np.concatenate((O_ins[2].reshape(1, 4), (prediction_HO * np.max(o_score))), axis=1)
                        Score_obj = np.concatenate((Score_obj, This_Score_obj), axis=0)
                if (Score_obj.shape[0] == 0):
                    continue
                max_idx = np.argmax(Score_obj, 0)[4:]
                for i in range(29):
                    if ((i == 3) or (i == 17) or (i == 22) or (i == 27)):
                        agent_name = (Action_dic_inv[i] + '_agent')
                        dic[agent_name] = (np.max(h_score) * prediction_H[i])
                        continue
                    if (i == 2):
                        agent_name = 'cut_agent'
                        dic[agent_name] = (np.max(h_score) * max(Score_obj[max_idx[2]][(4 + 2)], Score_obj[max_idx[4]][(4 + 4)]))
                        continue
                    if (i == 4):
                        continue
                    if (i == 9):
                        agent_name = 'eat_agent'
                        dic[agent_name] = (np.max(h_score) * max(Score_obj[max_idx[9]][(4 + 9)], Score_obj[max_idx[16]][(4 + 16)]))
                        continue
                    if (i == 16):
                        continue
                    if (i == 19):
                        agent_name = 'hit_agent'
                        dic[agent_name] = (np.max(h_score) * max(Score_obj[max_idx[19]][(4 + 19)], Score_obj[max_idx[20]][(4 + 20)]))
                        continue
                    if (i == 20):
                        continue
                    if (i == 6):
                        agent_name = 'talk_on_phone_agent'
                        dic[agent_name] = (np.max(h_score) * Score_obj[max_idx[i]][(4 + i)])
                        continue
                    if (i == 8):
                        agent_name = 'work_on_computer_agent'
                        dic[agent_name] = (np.max(h_score) * Score_obj[max_idx[i]][(4 + i)])
                        continue
                    agent_name = (Action_dic_inv[i].split('_')[0] + '_agent')
                    dic[agent_name] = (np.max(h_score) * Score_obj[max_idx[i]][(4 + i)])
                for i in range(29):
                    if ((i == 3) or (i == 17) or (i == 22) or (i == 27)):
                        dic[Action_dic_inv[i]] = np.append(np.full(4, np.nan).reshape(1, 4), (np.max(h_score) * prediction_H[i]))
                        continue
                    if ((H_ins[4] * Score_obj[max_idx[i]][(4 + i)]) == 0):
                        dic[Action_dic_inv[i]] = np.append(np.full(4, np.nan).reshape(1, 4), (np.max(h_score) * Score_obj[max_idx[i]][(4 + i)]))
                    else:
                        dic[Action_dic_inv[i]] = np.append(Score_obj[max_idx[i]][:4], (np.max(h_score) * Score_obj[max_idx[i]][(4 + i)]))
                detection.append(dic)
        _t['im_detect'].toc()
        print('im_detect: {:d}/{:d} {:.3f}s'.format((count + 1), 4946, _t['im_detect'].average_time))
        count += 1
    pickle.dump(detection, open(output_file, 'wb'))
