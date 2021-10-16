import sys
from math import sqrt, floor


def how_many_primes(n: int, size: int) -> int:
    if n <= 1:
        return 0
    if n == 2:
        return 1
    if n == 3:
        return 2

    assert size >= 1

    # common

    s = floor(sqrt(n))

    tab = [True] * (s+1)

    for i in range(2, s):
        if tab[i]:
            for j in range(2*i, s+1, i):
                tab[j] = False

    tab[0] = tab[1] = False

    primes1 = [i for i, is_prime in enumerate(tab) if is_prime]
    count = len(primes1)
    # primes2 = []

    s += 1
    if s % 2 == 0:
        s += 1

    for rank in range(size):
        # single

        for i in range(s+2*rank, n+1, 2*size):
            for p1 in primes1:
                if i % p1 == 0:
                    break
            else:
                # primes2.append(i)
                count += 1

    # primes2.sort()
    # print(primes1 + primes2)
    return count


if __name__ == '__main__':
    assert len(sys.argv) == 3
    n = int(sys.argv[1])
    size = int(sys.argv[2])
    print(how_many_primes(n, size))
