#!/bin/bash

#SBATCH --job-name=pros-translate
#SBATCH --output=translate_output.txt
#SBATCH --error=translate_error.txt
#SBATCH --time=02:00:00
#SBATCH --partition=short_mdbf
#SBATCH --qos=short_mdbf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=28

module load python
python tmp.py