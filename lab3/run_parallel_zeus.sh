#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 4
#SBATCH --time=01:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus

module add plgrid/tools/python-intel/3.6.5 2>/dev/null

mpiexec -np 4 ./parallel.py
