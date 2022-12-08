import math


def isPrime(n):
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True
    else:
        return False


num = 3
if isPrime(num):
    print("YES")
else:
    print("NO")
