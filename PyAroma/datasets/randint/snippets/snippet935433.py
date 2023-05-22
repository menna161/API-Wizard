import sys
import time
import uuid
import numpy as np
import random
import numpy as np


def follower(cloudburst, exec_id, my_id):
    import random
    val = random.randint(0, 100)
    key = ('%s-%d' % (exec_id, my_id))
    cloudburst.put(key, val)
    return (key, my_id, val)
