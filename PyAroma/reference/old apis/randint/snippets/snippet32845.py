import rsa.randnum
import doctest


def miller_rabin_primality_testing(n, k):
    "Calculates whether n is composite (which is always correct) or prime\n    (which theoretically is incorrect with error probability 4**-k), by\n    applying Miller-Rabin primality testing.\n\n    For reference and implementation example, see:\n    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test\n\n    :param n: Integer to be tested for primality.\n    :type n: int\n    :param k: Number of rounds (witnesses) of Miller-Rabin testing.\n    :type k: int\n    :return: False if the number is composite, True if it's probably prime.\n    :rtype: bool\n    "
    if (n < 2):
        return False
    d = (n - 1)
    r = 0
    while (not (d & 1)):
        r += 1
        d >>= 1
    for _ in range(k):
        a = (rsa.randnum.randint((n - 4)) + 2)
        x = pow(a, d, n)
        if ((x == 1) or (x == (n - 1))):
            continue
        for _ in range((r - 1)):
            x = pow(x, 2, n)
            if (x == 1):
                return False
            if (x == (n - 1)):
                break
        else:
            return False
    return True
