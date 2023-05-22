import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import *
import ipywidgets as widgets
import whynot as wn
from whynot.dynamics import DynamicsExperiment
from whynot.simulators import opioid
from whynot.simulators.opioid.experiments import sample_initial_states, opioid_intervention, overdose_deaths
from whynot_estimators import causal_forest
from matplotlib import rc


def generate_data(data_dir='heterogeneous_example_data', verbose=True):
    if (data_dir[(- 1)] != '/'):
        data_dir += '/'
    if (not os.path.exists(data_dir)):
        os.makedirs(data_dir)
    data_filename = (data_dir + 'heterogeneous_example_data.json')
    sample_sizes = [100, 200, 500, 1000, 2000]
    illicit_exits = np.arange(0.28, (0.36 + 1e-06), 0.04)
    nonmedical_incidence_deltas = np.arange((- 0.12), ((- 0.1) + 1e-06), 0.01)
    try:
        data = json.load(open(data_filename))
        print('DATA FILE FOUND')
    except:
        print('DATA FILE NOT FOUND')
        data = {}
    for n in sample_sizes:
        data[str(n)] = data.get(str(n), {})
        for illicit_exit in illicit_exits:
            key = '{:.2f}'.format(illicit_exit)
            data[str(n)][key] = data.get(key, {})
            for delta in nonmedical_incidence_deltas:
                key_ = '{:.2f}'.format(delta)
                data[str(n)][key][key_] = data[str(n)][key].get(key_, {})
    for n in sample_sizes:
        for (i, illicit_exit) in enumerate(illicit_exits):
            for (j, delta) in enumerate(nonmedical_incidence_deltas):
                one_run_data = data[str(n)]['{:.2f}'.format(illicit_exit)]['{:.2f}'.format(delta)]
                if ('true_effects' in one_run_data):
                    continue
                if verbose:
                    sim_number = (((i * len(illicit_exits)) + j) + 1)
                    total_num_sims = (len(illicit_exits) * len(nonmedical_incidence_deltas))
                    if (sim_number == 1):
                        print('\nSIMULATING: SAMPLE SIZE {}'.format(n))
                    print('  Running simulation {}/{}'.format(sim_number, total_num_sims))
                experiment = DynamicsExperiment(name='opioid_rct', description='Randomized experiment reducing nonmedical incidence of opioid use in 2015.', simulator=opioid, simulator_config=opioid.Config(illicit_exit=illicit_exit), intervention=opioid_intervention, state_sampler=sample_initial_states, propensity_scorer=0.5, outcome_extractor=overdose_deaths, covariate_builder=(lambda run: run.initial_state.values()))
                d = experiment.run(num_samples=n, nonmedical_incidence_delta=delta)
                one_run_data['covariates'] = tuple((tuple(x) for x in d.covariates.astype(float)))
                one_run_data['treatments'] = tuple(d.treatments.astype(float))
                one_run_data['outcomes'] = tuple(d.outcomes.astype(float))
                one_run_data['true_effects'] = tuple(d.true_effects.astype(float))
    json.dump(data, open(data_filename, 'w'))
    for n in sample_sizes:
        for (i, illicit_exit) in enumerate(illicit_exits):
            for (j, delta) in enumerate(nonmedical_incidence_deltas):
                one_run_data = data[str(n)]['{:.2f}'.format(illicit_exit)]['{:.2f}'.format(delta)]
                if ('estimated_effects' in one_run_data):
                    continue
                if verbose:
                    sim_number = (((i * len(illicit_exits)) + j) + 1)
                    total_num_sims = (len(illicit_exits) * len(nonmedical_incidence_deltas))
                    if (sim_number == 1):
                        print('\nESTIMATING: SAMPLE SIZE {}'.format(n))
                    print('  Running estimation {}/{}'.format(sim_number, total_num_sims))
                estimate = causal_forest.estimate_treatment_effect(np.array(one_run_data['covariates']), np.array(one_run_data['treatments']), np.array(one_run_data['outcomes']))
                one_run_data['estimated_effects'] = tuple(estimate.individual_effects)
    json.dump(data, open(data_filename, 'w'))
