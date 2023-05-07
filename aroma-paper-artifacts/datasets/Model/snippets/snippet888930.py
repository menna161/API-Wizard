import dataclasses
import os
import numpy as np
from py_mini_racer import py_mini_racer
import whynot as wn
from whynot.dynamics import BaseConfig, BaseState, BaseIntervention


def set_state(js_context, initial_state):
    'Set the state of the world3 simulator.'
    for (stock_name, value) in dataclasses.asdict(initial_state).items():
        js_context.eval(f'{to_camel_case(stock_name)}.initVal = {value}')
    js_context.eval(f'nonrenewableResourcesInitialK = {initial_state.nonrenewable_resources}')
    js_context.eval('resetModel()')
