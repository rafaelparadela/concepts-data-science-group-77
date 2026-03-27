#!/bin/bash
#SBATCH --job-name=bloom_benchmark
#SBATCH --output=benchmarks/benchmark_output.txt
#SBATCH --error=benchmarks/benchmark_error.txt
#SBATCH --time=00:10:00
#SBATCH --mem=2G

module load Python/3.12.1

python -m benchmarks.benchmark