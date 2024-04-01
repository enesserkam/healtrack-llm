#!/bin/bash

#SBATCH --job-name=llm-chat
#SBATCH --output=job_output.txt
#SBATCH --error=job_error.txt
#SBATCH --time=02:00:00
#SBATCH --partition=short_mdbf
#SBATCH --qos=short_mdbf
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G

module load python
source /cta/users/eonus/projects/llm_model/bin/activate
python gguf_7b.py
deactivate
