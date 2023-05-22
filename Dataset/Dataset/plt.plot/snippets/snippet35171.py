import os
import torch
import json
import paddle.fluid as fluid
import matplotlib.pyplot as plt


def draw_roc(frr_list, far_list, roc_auc):
    plt.switch_backend('agg')
    plt.rcParams['figure.figsize'] = (6.0, 6.0)
    plt.title('ROC')
    plt.plot(far_list, frr_list, 'b', label=('AUC = %0.4f' % roc_auc))
    plt.legend(loc='upper right')
    plt.plot([0, 1], [1, 0], 'r--')
    plt.grid(ls='--')
    plt.ylabel('False Negative Rate')
    plt.xlabel('False Positive Rate')
    save_dir = './work_dir/ROC/'
    if (not os.path.exists(save_dir)):
        os.makedirs(save_dir)
    plt.savefig('./work_dir/ROC/ROC.png')
    file = open('./work_dir/ROC/FAR_FRR.txt', 'w')
    save_json = []
    dict = {}
    dict['FAR'] = far_list
    dict['FRR'] = frr_list
    save_json.append(dict)
    json.dump(save_json, file, indent=4)
