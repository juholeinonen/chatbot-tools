#!/bin/bash -e

#SBATCH --partition gpu
#SBATCH --time=80:00:00
#SBATCH --mem=16G
#SBATCH --gres=gpu:1
#SBATCH -o /scratch/work/jpleino1/log/chatbot-%j.log
#SBATCH -e /scratch/work/jpleino1/log/chatbot-%j.log

module purge
module load anaconda3
source activate /scratch/work/jpleino1/conda/envs/parlai

python -m parlai.scripts.train_model -m seq2seq -t convai2:SelfOriginalTeacher:no_cands -bs 64 -ttim 252000 -vp 10 -mf models/s2s_convai2_en_word
