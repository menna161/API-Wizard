import argparse
import collections
import datetime
import enum
import io
import os
import os.path as osp
import re
import crayons
import numpy as np
import rpyc
import tqdm
from asnets.multiprob import ProblemServer
from asnets.prof_utils import can_profile
from asnets.py_utils import remove_cycles
from asnets.scripts.run_asnets import get_problem_names
from asnets.ssipp_interface import Cutter
from asnets.state_reprs import sample_next_state, get_init_cstate
from asnets.supervised import ProblemServiceConfig, PlannerExtensions
import matplotlib.pyplot as plt
import matplotlib.offsetbox as obox
import matplotlib.ticker as tick
import matplotlib.pyplot as plt
from asnets.teacher import DomainSpecificTeacher
import matplotlib.pyplot as plt


def main_plan(args, planner_exts):
    import matplotlib.pyplot as plt
    actions = parse_gm_plan_file(args.plan)
    if (args.max_cycle_repeat > 0):
        (actions, num_removed) = remove_cycles(actions, max_cycle_len=3, max_cycle_repeats=args.max_cycle_repeat)
        if (num_removed > 0):
            print(('Trimmed out %d actions from cycle at end of plan' % num_removed))
    state = get_init_cstate(planner_exts)
    gm_images = [render_gm_state(state)]
    for action in tqdm.tqdm(actions):
        name_to_id = {act.unique_ident: idx for (idx, (act, _)) in enumerate(state.acts_enabled)}
        to_choose = name_to_id[action]
        (state, _) = sample_next_state(state, to_choose, planner_exts)
        gm_images.append(render_gm_state(state))
    basename = osp.basename(args.plan)
    time_str = datetime.datetime.now().isoformat()
    out_dir = osp.join(args.out_dir, ('render-%s-%s' % (basename, time_str)))
    os.makedirs(out_dir, exist_ok=True)
    print(("Writing frames to '%s':" % out_dir))
    for (step, action) in enumerate((['init'] + actions)):
        out_path = osp.join(out_dir, ('%03i-%s.png' % (step, action)))
        print(("    -> Writing '%s'" % out_path))
        plt.imsave(out_path, gm_images[step], vmin=0.0, vmax=1.0)
