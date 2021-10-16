#!/usr/bin/env python
import numpy as np
import sys
from math import sqrt, floor
from mpi4py import MPI


if __name__ == '__main__':
    assert len(sys.argv) == 2
    n = int(sys.argv[1])
    assert n >= 4

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    s = floor(sqrt(n))

    tab = [True] * (s+1)

    for i in range(2, s):
        if tab[i]:
            for j in range(2*i, s+1, i):
                tab[j] = False

    tab[0] = tab[1] = False

    primes1 = [i for i, is_prime in enumerate(tab) if is_prime]
    # primes2 = []

    s += 1
    if s % 2 == 0:
        s += 1

    count = 0

    for i in range(s+2*rank, n+1, 2*size):
        for p1 in primes1:
            if i % p1 == 0:
                break
        else:
            # primes2.append(i)
            count += 1

    count = np.array(count, 'i')
    count_sum = np.array(0, 'i')
    comm.Reduce(count, count_sum, op=MPI.SUM, root=0)

    if rank == 0:
        result = len(primes1) + count_sum
        print(result)
