#!/bin/bash
#SBATCH --partition batch
#SBATCH --time=12:00:00    # 6 hours
#SBATCH --mem-per-cpu=60000    # 1024MB of memory
#SBATCH -o /scratch/work/jpleino1/log/morfessor-%j.log
#SBATCH -e /scratch/work/jpleino1/log/morfessor-%j.log


if [ $# != 1 ]; then

  echo "Give the text file"
  exit 1;
fi

text=$1
num_morphs=75000
compound=none         #This is a guess
format="{analysis} "
separator="+ +"

morfessor-train --encoding=utf-8 --logfile=Morfessor_log.log --num-morph-types=$num_morphs -s Morfessor.bin -d $compound $text

LC_ALL= morfessor-segment -l Morfessor.bin --output-format="$format" --output-format-separator "$separator" --output-newlines $text > ${text}_segmented
