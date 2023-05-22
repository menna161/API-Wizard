import numpy as np
from terminaltables import AsciiTable
from .bbox_overlaps import bbox_overlaps
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def plot_num_recall(recalls, proposal_nums):
    'Plot Proposal_num-Recalls curve.\n\n    Args:\n        recalls(ndarray or list): shape (k,)\n        proposal_nums(ndarray or list): same shape as `recalls`\n    '
    if isinstance(proposal_nums, np.ndarray):
        _proposal_nums = proposal_nums.tolist()
    else:
        _proposal_nums = proposal_nums
    if isinstance(recalls, np.ndarray):
        _recalls = recalls.tolist()
    else:
        _recalls = recalls
    import matplotlib.pyplot as plt
    f = plt.figure()
    plt.plot(([0] + _proposal_nums), ([0] + _recalls))
    plt.xlabel('Proposal num')
    plt.ylabel('Recall')
    plt.axis([0, proposal_nums.max(), 0, 1])
    f.show()
