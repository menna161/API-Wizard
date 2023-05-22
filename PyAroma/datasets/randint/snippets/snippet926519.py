import argparse
import gin
import os
import util
import numpy as np
import multiprocessing as mp
import cma


def main(config):
    logger = util.create_logger(name='train_log', log_dir=config.log_dir)
    if (not os.path.exists(config.log_dir)):
        os.makedirs(config.log_dir, exist_ok=True)
    util.save_config(config.log_dir, config.config)
    logger.info('Logs and models will be save in {}.'.format(config.log_dir))
    rnd = np.random.RandomState(seed=config.seed)
    solution = util.create_solution(device='cpu:0')
    num_params = solution.get_num_params()
    if (config.load_model is not None):
        solution.load(config.load_model)
        print('Loaded model from {}'.format(config.load_model))
        init_params = solution.get_params()
    else:
        init_params = None
    solver = cma.CMAEvolutionStrategy(x0=(np.zeros(num_params) if (init_params is None) else init_params), sigma0=config.init_sigma, inopts={'popsize': config.population_size, 'seed': (config.seed if (config.seed > 0) else 42), 'randn': np.random.randn})
    best_so_far = (- float('Inf'))
    ii32 = np.iinfo(np.int32)
    repeats = ([config.reps] * config.population_size)
    device_type = ('cpu' if (args.num_gpus <= 0) else 'cuda')
    num_devices = (mp.cpu_count() if (args.num_gpus <= 0) else args.num_gpus)
    with mp.get_context('spawn').Pool(initializer=worker_init, initargs=(args.config, device_type, num_devices), processes=config.num_workers) as pool:
        for n_iter in range(config.max_iter):
            params_set = solver.ask()
            task_seeds = ([rnd.randint(0, ii32.max)] * config.population_size)
            fitnesses = []
            ss = 0
            while (ss < config.population_size):
                ee = (ss + min(config.num_workers, (config.population_size - ss)))
                fitnesses.append(pool.map(func=get_fitness, iterable=zip(params_set[ss:ee], task_seeds[ss:ee], repeats[ss:ee])))
                ss = ee
            fitnesses = np.concatenate(fitnesses)
            if isinstance(solver, cma.CMAEvolutionStrategy):
                solver.tell(params_set, (- fitnesses))
            else:
                solver.tell(fitnesses)
            logger.info('Iter={0}, max={1:.2f}, avg={2:.2f}, min={3:.2f}, std={4:.2f}'.format(n_iter, np.max(fitnesses), np.mean(fitnesses), np.min(fitnesses), np.std(fitnesses)))
            best_fitness = max(fitnesses)
            if (best_fitness > best_so_far):
                best_so_far = best_fitness
                model_path = os.path.join(config.log_dir, 'best.npz')
                save_params(solver=solver, solution=solution, model_path=model_path)
                logger.info('Best model updated, score={}'.format(best_fitness))
            if (((n_iter + 1) % config.save_interval) == 0):
                model_path = os.path.join(config.log_dir, 'iter_{}.npz'.format((n_iter + 1)))
                save_params(solver=solver, solution=solution, model_path=model_path)
