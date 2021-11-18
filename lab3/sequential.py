#!/usr/bin/env python

import numpy as np

if __name__ == '__main__':
    g = 1
    h = 0.1
    lambda_ = 1

    N = 200
    number_of_iterations = 200
    dtype = np.float64

    gh2over4lambda = (g * h ** 2) / (4 * lambda_)

    T = np.zeros((N+2, N+2), dtype=dtype)

    # boundary conditions
    T[0, :] = T[N+1, :] = T[:, 0] = T[:, N+1] = 0

    # initial values
    T[70+1:130+1, 70+1:130+1] = 5

    prev = T.copy()
    for _ in range(number_of_iterations):
        # double buffering
        prev, T = T, prev

        # calculate single step
        for i in range(1, N+1):
            for j in range(1, N+1):
                T[i, j] = (prev[i+1, j] + prev[i-1, j] + prev[i, j+1] + prev[i, j-1]) / 4 + gh2over4lambda

    # remove boundaries
    T = T[1:N+1, 1:N+1]

    np.save('output.npy', T)
