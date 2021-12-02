#!/usr/bin/env python
import numpy as np
from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
from timeit import default_timer as timer

x0, x1, w = -2.0, +2.0, 640*2
y0, y1, h = -1.5, +1.5, 480*2
dx = (x1 - x0) / w
dy = (y1 - y0) / h

c = complex(0, 0.65)

def julia(x, y):
    z = complex(x, y)
    n = 255
    while abs(z) < 3 and n > 1:
        z = z**2 + c
        n -= 1
    return n

def julia_line(k):
    rank = MPI.COMM_WORLD.Get_rank()
    start = timer()
    line = bytearray(w)
    y = y1 - k * dy
    for j in range(w):
        x = x0 + j * dx
        line[j] = julia(x, y)
    if k == 42:
        np.fft.fft(np.random.rand(6000, 6000))
    end = timer()
    print(f'{k},{rank},{end - start}')
    return line

if __name__ == '__main__':
    with MPIPoolExecutor() as executor:
        image = executor.map(julia_line, range(h))
        with open('julia.pgm', 'wb') as f:
            f.write(b'P5 %d %d %d\n' % (w, h, 255))
            for line in image:
                f.write(line)
