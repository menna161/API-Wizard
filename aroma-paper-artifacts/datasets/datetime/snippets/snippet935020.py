import csv
import datetime
import os


def __init__(self, name_to_save, continue_experiment, save_images):
    self._dict_summary = {'exp_id': (- 1), 'rep': (- 1), 'weather': (- 1), 'start_point': (- 1), 'end_point': (- 1), 'result': (- 1), 'initial_distance': (- 1), 'final_distance': (- 1), 'final_time': (- 1), 'time_out': (- 1), 'end_pedestrian_collision': (- 1), 'end_vehicle_collision': (- 1), 'end_other_collision': (- 1), 'number_red_lights': (- 1), 'number_green_lights': (- 1)}
    self._dict_measurements = {'exp_id': (- 1), 'rep': (- 1), 'weather': (- 1), 'start_point': (- 1), 'end_point': (- 1), 'collision_other': (- 1), 'collision_pedestrians': (- 1), 'collision_vehicles': (- 1), 'intersection_otherlane': (- 1), 'intersection_offroad': (- 1), 'pos_x': (- 1), 'pos_y': (- 1), 'steer': (- 1), 'throttle': (- 1), 'brake': (- 1)}
    if (not os.path.exists('_benchmarks_results')):
        os.mkdir('_benchmarks_results')
    self._path = os.path.join('_benchmarks_results', name_to_save)
    (self._path, _, self._summary_fieldnames, self._measurements_fieldnames) = self._continue_experiment(continue_experiment)
    self._create_log_files()
    now = datetime.datetime.now()
    self._internal_log_name = os.path.join(self._path, ('log_' + now.strftime('%Y%m%d%H%M')))
    open(self._internal_log_name, 'w').close()
    self._save_images = save_images
    self._image_filename_format = os.path.join(self._path, '_images/episode_{:s}/{:s}/image_{:0>5d}.jpg')
