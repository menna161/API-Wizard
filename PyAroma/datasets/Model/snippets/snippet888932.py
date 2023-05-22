import dataclasses
import os
import numpy as np
from py_mini_racer import py_mini_racer
import whynot as wn
from whynot.dynamics import BaseConfig, BaseState, BaseIntervention


def set_config(js_context, config, intervention):
    'Set the non-state variables of the world3 simulator.'
    js_context.eval(f'startTime = {config.start_time}')
    js_context.eval(f'stopTime = {config.end_time}')
    js_context.eval(f'dt = {config.delta_t}')
    if intervention:
        intervention_config = config.update(intervention)
        js_context.eval(f'policyYear = {intervention.time}')
    else:
        intervention_config = config
        js_context.eval(f'policyYear = {config.end_time}')
    intervention_config = dataclasses.asdict(intervention_config)
    for (parameter, before) in dataclasses.asdict(config).items():
        if (parameter in ['policy_year', 'start_time', 'end_time', 'delta_t']):
            continue
        after = intervention_config[parameter]
        js_context.eval(f'{to_camel_case(parameter)}.before = {before}')
        js_context.eval(f'{to_camel_case(parameter)}.after = {after}')
    js_context.eval('resetModel()')
