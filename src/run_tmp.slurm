#!/bin/bash

#SBATCH --job-name=my_temp_job
#SBATCH --output=job_output.txt
#SBATCH --error=job_error.txt
#SBATCH --time=01:00:00
#SBATCH --partition=short_mdbf
#SBATCH --qos=short_mdbf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

module load python
python tmp.py
