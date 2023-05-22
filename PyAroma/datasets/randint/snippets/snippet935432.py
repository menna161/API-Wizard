import sys
import time
import uuid
import numpy as np
import random
import numpy as np


def run(cloudburst_client, num_requests, sckt):
    ' DEFINE AND REGISTER FUNCTIONS '

    def follower(cloudburst, exec_id, my_id):
        import random
        val = random.randint(0, 100)
        key = ('%s-%d' % (exec_id, my_id))
        cloudburst.put(key, val)
        return (key, my_id, val)

    def leader(cloudburst, exec_id, num_execs):
        values = []
        for i in range(num_execs):
            key = ('%s-%d' % (exec_id, i))
            result = cloudburst.get(key)
            while (result is None):
                result = cloudburst.get(key)
            values.append(result)
        import numpy as np
        return np.mean(values)
    cloud_follow = cloudburst_client.register(follower, 'follower')
    cloud_lead = cloudburst_client.register(leader, 'leader')
    if (cloud_follow and cloud_lead):
        print('Successfully registered follower and leader functions.')
    else:
        sys.exit(1)
    ' TEST REGISTERED FUNCTIONS '
    n = 5
    latencies = []
    for _ in range(num_requests):
        time.sleep(2)
        start = time.time()
        uid = str(uuid.uuid4())
        for i in range(n):
            res = cloud_follow(uid, i)
        result = cloud_lead(uid, n)
        end = time.time()
        latencies.append((end - start))
    return (latencies, [], [], 0)
