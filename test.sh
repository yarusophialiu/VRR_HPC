#!/bin/bash
#SBATCH -A MANTIUK-SL3-CPU

#SBATCH --mem=3G
#SBATCH -D /home/yl962/rds/hpc-work/VRR/
#SBATCH -o logs/encode.log
#SBATCH -t 00:01:00 # Time limit (hh:mm:ss)
#SBATCH -a 1-5

# module load cuda/12.1 cudnn/8.9_cuda-12.1
module load ceuadmin/ffmpeg/5.1.1

output=$(ffmpeg -codecs | grep "hevc")
echo "This task number $SLURM_ARRAY_TASK_ID"
echo "Using "
echo

# Run the Python script
python enc_video_HPC.py $SLURM_ARRAY_TASK_ID