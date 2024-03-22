#!/bin/bash

#SBATCH --job-name=my_temp_job # Job name
#SBATCH --output=job_output.txt   # Output file
#SBATCH --error=job_error.txt     # Error file
#SBATCH --time=01:00:00           # Time limit hrs:min:sec
#SBATCH --partition=debug      # Partition to submit to
#SBATCH --ntasks=1                # Number of tasks (processes)
#SBATCH --cpus-per-task=1         # Number of CPU cores per task
#SBATCH --mem=1G                  # Memory (RAM) per process

module load python                # Load the python module, adjust if needed
python tmp.py               # Execute the Python script
