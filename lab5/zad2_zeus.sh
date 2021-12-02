#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=01:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus

module add plgrid/tools/python-intel/3.6.5 2>/dev/null

echo "k,rank,time"

mpiexec -np 1 -usize 8 ./zad2.py
