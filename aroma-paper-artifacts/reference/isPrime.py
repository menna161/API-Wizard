import math


def isPrime(n):
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True
    else:
        return False


def isPrime2(n):
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % 2 == 0:
            return False
    return True


def isPrime3(n):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True


num = 3
if isPrime(num):
    print("YES")
else:
    print("NO")
