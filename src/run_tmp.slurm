#!/bin/bash

#SBATCH --job-name=llm-chat
#SBATCH --output=job_output.txt
#SBATCH --error=job_error.txt
#SBATCH --time=01:00:00
#SBATCH --partition=short_mdbf
#SBATCH --qos=short_mdbf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G

module load python
python tmp.py

