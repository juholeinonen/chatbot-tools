#!/bin/bash -e

#SBATCH --partition gpu
#SBATCH --time=120:00:00
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH -o /scratch/work/jpleino1/log/chatbot-%j.log
#SBATCH -e /scratch/work/jpleino1/log/chatbot-%j.log

module purge
module load anaconda3
source activate /scratch/work/jpleino1/conda/envs/parlai

python -m parlai.scripts.train_model -m seq2seq -t opensubtitles:V2018Teacher -bs 32 -ttim 360000 -vp 10 -mf models/s2s_movies_en_word_bs64
