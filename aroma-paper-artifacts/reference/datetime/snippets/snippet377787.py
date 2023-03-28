import csv
import datetime
import os
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import pandas as pd


def write_gs_param_results_to_file(trained_gs, most_recent_filename):
    timestamp_time = datetime.datetime.now()
    write_most_recent_gs_result_to_file(trained_gs, most_recent_filename, timestamp_time)
    grid_scores = trained_gs.grid_scores_
    scorer = trained_gs.scorer_
    best_score = trained_gs.best_score_
    file_name = 'pipeline_grid_search_results.csv'
    write_header = False
    if (not os.path.isfile(file_name)):
        write_header = True
    with open(file_name, 'a') as results_file:
        writer = csv.writer(results_file, dialect='excel')
        if write_header:
            writer.writerow(['timestamp', 'scorer', 'best_score', 'all_grid_scores'])
        writer.writerow([timestamp_time, scorer, best_score, grid_scores])
