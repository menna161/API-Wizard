import math
import sys
import os
import paddle.fluid as fluid
import mlflow
from paddle.fluid.incubate.fleet.parameter_server.distribute_transpiler import fleet
from paddle.fluid.incubate.fleet.base import role_maker
from paddle.fluid.transpiler.distribute_transpiler import DistributeTranspilerConfig
from paddle.fluid.contrib.utils.hdfs_utils import HDFSClient
from nets import ctr_dnn_model
import subprocess as sp
import time
import psutil
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
from datetime import datetime, timedelta
import json
import logging


def handler(self, fetch_target_vars):
    auc = fetch_target_vars[0]
    print('test metric auc: ', fetch_target_vars)
    global last_net_sent
    global last_net_recv
    global y_auc
    global y_cpu
    global y_memory
    global y_network_sent
    global y_network_recv
    global x
    mlflow.log_metric('network_bytes_sent_speed', (psutil.net_io_counters().bytes_sent - last_net_sent))
    mlflow.log_metric('network_bytes_recv_speed', (psutil.net_io_counters().bytes_recv - last_net_recv))
    y_network_sent.append(((psutil.net_io_counters().bytes_sent - last_net_sent) / 10))
    y_network_recv.append(((psutil.net_io_counters().bytes_recv - last_net_recv) / 10))
    last_net_sent = psutil.net_io_counters().bytes_sent
    last_net_recv = psutil.net_io_counters().bytes_recv
    mlflow.log_metric('cpu_usage_total', round((psutil.cpu_percent(interval=0) / 100), 3))
    y_cpu.append(round((psutil.cpu_percent(interval=0) / 100), 3))
    mlflow.log_metric('free_memory/GB', round((psutil.virtual_memory().free / ((1024.0 * 1024.0) * 1024.0)), 3))
    mlflow.log_metric('memory_usage', round(((psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)), 3))
    y_memory.append(round(((psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total)), 3))
    if (auc == None):
        mlflow.log_metric('auc', 0.5)
        auc = [0.5]
    else:
        mlflow.log_metric('auc', auc[0])
    y_auc.append(auc)
    x_list.append(x)
    if (x >= 120):
        y_auc.pop(0)
        y_cpu.pop(0)
        y_memory.pop(0)
        y_network_recv.pop(0)
        y_network_sent.pop(0)
        x_list.pop(0)
    x += 10
    if (((x % 60) == 0) and (x != 0)):
        plt.subplot(221)
        plt.plot(x_list, y_auc)
        plt.title('auc')
        plt.grid(True)
        plt.subplot(222)
        plt.plot(x_list, y_cpu)
        plt.title('cpu_usage')
        plt.grid(True)
        plt.subplot(223)
        plt.plot(x_list, y_memory)
        plt.title('memory_usage')
        plt.grid(True)
        plt.subplot(224)
        plt.plot(x_list, y_network_sent, label='network_sent_speed')
        plt.plot(x_list, y_network_recv, label='network_recv_speed')
        plt.title('network_speed')
        plt.grid(True)
        plt.subplots_adjust(top=0.9, bottom=0.2, hspace=0.4, wspace=0.35)
        plt.legend(bbox_to_anchor=(0, (- 0.6)), loc='lower left', borderaxespad=0.0)
        temp_file_name = (('dashboard_' + time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))) + '.png')
        plt.savefig(temp_file_name, dpi=250)
        sys.stdout.flush()
        plt.clf()
        os.system((('rm -f ' + str(mlflow.get_artifact_uri().split(':')[1])) + '/*.png'))
        mlflow.log_artifact(local_path=temp_file_name)
        sys.stdout.flush()
        os.system('rm -f ./*.png')
        sys.stdout.flush()
        logger.info(str(mlflow.get_artifact_uri().split(':')[1]))
        sys.stdout.flush()
