import random
import math


def __call__(self, frame_indices):
    '\n        Args:\n            frame_indices (list): frame indices to be cropped.\n        Returns:\n            list: Cropped frame indices.\n        '
    rand_end = max(0, ((len(frame_indices) - self.size) - 1))
    begin_index = random.randint(0, rand_end)
    end_index = min((begin_index + self.size), len(frame_indices))
    out = frame_indices[begin_index:end_index]
    for index in out:
        if (len(out) >= self.size):
            break
        out.append(index)
    return out
