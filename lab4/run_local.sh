#!/usr/bin/env bash

echo "i,problem_size,np,N,number_of_iterations,time"

number_of_iterations=20

for i in {1..5} ; do
    for K in {1..2} ; do
        for problem_size in 100 150 200 ; do
            N=$((problem_size / K))
            np=$((K * K))
            echo -n "$i,$problem_size,$np,$N,$number_of_iterations,"
            mpiexec -np $np python3 parallel.py $N $number_of_iterations 2>/dev/null
        done
    done
done
