import os
import numpy as np
from visualization.data_reading import read_control_csv, read_summary_csv
from configs.coil_global import get_names, merge_with_yaml, g_conf


def export_csv_separate(exp_batch, variables_to_export, task_list):
    root_path = '_logs'
    experiments = os.listdir(os.path.join(root_path, exp_batch))
    if ('episodes_fully_completed' not in set(variables_to_export)):
        raise ValueError(' export csv needs the episodes fully completed param on variables')
    csv_outfile = os.path.join(root_path, exp_batch, 'result.csv')
    with open(csv_outfile, 'w') as f:
        f.write('experiment,environment')
        for variable in variables_to_export:
            f.write((',%s' % variable))
        f.write('\n')
    experiment_list = []
    for exp in experiments:
        if os.path.isdir(os.path.join(root_path, exp_batch, exp)):
            experiments_logs = os.listdir(os.path.join(root_path, exp_batch, exp))
            scenario = []
            for log in experiments_logs:
                dicts_to_write = {}
                for task in task_list:
                    dicts_to_write.update({task: {}})
                for task in task_list:
                    if (('drive' in log) and ('_csv' in log)):
                        csv_file_path = os.path.join(root_path, exp_batch, exp, log, (('control_output_' + task) + '.csv'))
                        if (not os.path.exists(csv_file_path)):
                            continue
                        control_csv = read_summary_csv(csv_file_path)
                        if (control_csv is None):
                            continue
                        print(control_csv)
                        position_of_max_success = np.argmax(control_csv['episodes_fully_completed'])
                        print(dicts_to_write)
                        for variable in variables_to_export:
                            dicts_to_write[task].update({variable: control_csv[variable][position_of_max_success]})
                scenario.append(dicts_to_write)
            experiment_list.append(scenario)
    print(' FULL DICT')
    print(experiment_list)
    with open(csv_outfile, 'a') as f:
        for exp in experiments:
            print('EXP ', exp)
            if os.path.isdir(os.path.join(root_path, exp_batch, exp)):
                experiments_logs = os.listdir(os.path.join(root_path, exp_batch, exp))
                count = 0
                for log in experiments_logs:
                    if (('drive' in log) and ('_csv' in log)):
                        f.write(('%s,%s' % (exp, log.split('_')[1])))
                        for variable in variables_to_export:
                            f.write(',')
                            for task in task_list:
                                if experiment_list[experiments.index(exp)][count][task]:
                                    f.write(('%.2f/' % experiment_list[experiments.index(exp)][count][task][variable]))
                        f.write('\n')
                    count += 1
