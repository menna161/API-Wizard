import numpy as np
from terminaltables import AsciiTable
from .bbox_overlaps import bbox_overlaps
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def print_recall_summary(recalls, proposal_nums, iou_thrs, row_idxs=None, col_idxs=None):
    'Print recalls in a table.\n\n    Args:\n        recalls(ndarray): calculated from `bbox_recalls`\n        proposal_nums(ndarray or list): top N proposals\n        iou_thrs(ndarray or list): iou thresholds\n        row_idxs(ndarray): which rows(proposal nums) to print\n        col_idxs(ndarray): which cols(iou thresholds) to print\n    '
    proposal_nums = np.array(proposal_nums, dtype=np.int32)
    iou_thrs = np.array(iou_thrs)
    if (row_idxs is None):
        row_idxs = np.arange(proposal_nums.size)
    if (col_idxs is None):
        col_idxs = np.arange(iou_thrs.size)
    row_header = ([''] + iou_thrs[col_idxs].tolist())
    table_data = [row_header]
    for (i, num) in enumerate(proposal_nums[row_idxs]):
        row = ['{:.3f}'.format(val) for val in recalls[(row_idxs[i], col_idxs)].tolist()]
        row.insert(0, num)
        table_data.append(row)
    table = AsciiTable(table_data)
    print(table.table)
