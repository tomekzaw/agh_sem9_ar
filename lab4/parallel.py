#!/usr/bin/env python

import sys
import numpy as np
from math import sqrt
from time import time
from mpi4py import MPI

if __name__ == '__main__':
    start = time()

    assert len(sys.argv) == 3

    g = 1
    h = 0.1
    lambda_ = 1

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    N = int(sys.argv[1])
    number_of_iterations = int(sys.argv[2])
    dtype = np.float64

    K = int(sqrt(size))
    assert size == K*K

    I = rank % K
    J = rank // K

    gh2over4lambda = (g * h ** 2) / (4 * lambda_)

    T = np.zeros((N+2, N+2), dtype=dtype)

    # boundary conditions
    T[0, :] = T[N+1, :] = T[:, 0] = T[:, N+1] = 0

    # initial values
    # if (I, J) == (0, 0):
    #     T[70+1:100+1, 70+1:100+1] = 5
    # if (I, J) == (0, 1):
    #     T[70+1:100+1, 0+1:30+1] = 5
    # if (I, J) == (1, 0):
    #     T[0+1:30+1, 70+1:100+1] = 5
    # if (I, J) == (1, 1):
    #     T[0+1:30+1, 0+1:30+1] = 5
    T[30:70, 30:70] = 5

    prev = T.copy()
    for _ in range(number_of_iterations):
        # communicate with neighbours
        if I > 0:
            comm.isend(T[1, 1:N+1], dest=rank-1)
            left = comm.irecv(source=rank-1)

        if I < K-1:
            comm.isend(T[N, 1:N+1], dest=rank+1)
            right = comm.irecv(source=rank+1)

        if J > 0:
            comm.isend(T[1:N+1, 1], dest=rank-K)
            up = comm.irecv(source=rank-K)

        if J < K-1:
            comm.isend(T[1:N+1, N], dest=rank+K)
            down = comm.irecv(source=rank+K)

        # update edges
        if I > 0:
            T[0, 1:N+1] = left.wait()

        if I < K-1:
            T[N+1, 1:N+1] = right.wait()

        if J > 0:
            T[1:N+1, 0] = up.wait()

        if J < K-1:
            T[1:N+1, N+1] = down.wait()

        # make sure that boundaries have been not changed
        # if I == 0:
        #     assert not T[0, 1:N+1].any()
        # if I == K-1:
        #     assert not T[N+1, 1:N+1].any()
        # if J == 0:
        #     assert not T[1:N+1, 0].any()
        # if J == K-1:
        #     assert not T[1:N+1, N+1].any()

        # double buffering
        prev, T = T, prev

        # calculate single step
        for i in range(1, N+1):
            for j in range(1, N+1):
                T[i, j] = (prev[i+1, j] + prev[i-1, j] + prev[i, j+1] + prev[i, j-1]) / 4 + gh2over4lambda

    # gather results in a single array of shape K*N x K*N
    Ts = comm.gather(T[1:N+1, 1:N+1])

    if rank == 0:  # root
        T = np.zeros((K*N, K*N), dtype=dtype)
        for I in range(K):
            for J in range(K):
                i = I*N
                j = J*N
                T[i:i+N, j:j+N] = Ts[I+J*K]

        # np.save('output.npy', T)

        end = time()
        print(end - start)
