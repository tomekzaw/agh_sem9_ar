#!/usr/bin/env python
from mpi4py import MPI
import sys

if __name__ == '__main__':
    is_root = (len(sys.argv) == 2)

    if is_root:
        n = int(sys.argv[1])
    else:
        comm_parent = MPI.Comm.Get_parent()
        n = comm_parent.recv(source=0)

    if n < 2:
        fibn = n
    else:
        comm_children = MPI.COMM_SELF.Spawn(
            sys.executable, args=['zad1.py'], maxprocs=2)
        comm_children.send(n - 1, dest=0)
        comm_children.send(n - 2, dest=1)
        x = comm_children.recv(source=0)
        y = comm_children.recv(source=1)
        fibn = x + y
        comm_children.Disconnect()

    if is_root:
        print(f'fib({n}) = {fibn}')
    else:
        comm_parent.send(fibn, dest=0)
        comm_parent.Disconnect()
