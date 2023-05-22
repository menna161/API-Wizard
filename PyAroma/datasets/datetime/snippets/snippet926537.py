from datetime import datetime
from utils import isnotebook, arr2img, save_as_gif, save_as_frames


def __call__(self, i, solver, fitness_fn, fitnesses_fn, best_params_fn):
    best_params = best_params_fn(solver)
    if self.fitnesses_fn_is_wrapper:
        cost = fitnesses_fn(fitness_fn, [best_params])
    else:
        cost = fitnesses_fn([best_params])
    print()
    print(f'[{datetime.now()}]   Iteration: {i}   cost: {cost}')
