#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 36
#SBATCH --time=04:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr21zeus

module add plgrid/tools/python-intel/3.6.5 2>/dev/null

echo "i,problem_size,np,N,number_of_iterations,time"

number_of_iterations=50

for i in {1..5} ; do
    for K in {6..1} ; do
        for problem_size in 50 200 2000 ; do
            np=$((K * K))
            N=$((problem_size / K))
            echo -n "$i,$problem_size,$np,$N,$number_of_iterations,"
            mpiexec -np $np python3 parallel.py $N $number_of_iterations 2>/dev/null
        done
    done
done
