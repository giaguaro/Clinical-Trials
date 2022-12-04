#!/bin/bash
#SBATCH --time=168-00:00
#SBATCH --cpus-per-task=60
#SBATCH --partition=normal
#SBATCH --job-name=icm_protacs_benchmarking
#SBATCH --ntasks=1

source ~/.bashrc
conda activate py39

unzip AllPublicXML.zip
