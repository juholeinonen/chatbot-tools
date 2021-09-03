#!/usr/bin/env python3
# coding: utf-8

# import libraries
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Preparing corpus for Transformer Language Model')
parser.add_argument('dataset', type=str,
                    help='The dataset to prepare')

args = parser.parse_args()

def makePairs():
    trainFileName, file_ext = os.path.splitext(args.dataset)

    qaFileName = trainFileName + "_QA" + file_ext

    with open(args.dataset, 'r', encoding='utf-8') as f_source, \
            open(qaFileName, 'w', encoding='utf-8') as f_target:
        previousA = "ihan hyvää"
        for line in f_source:
            if "persona:" in line:
                continue
            qaParts = line.rstrip().split('\t')
            qaParts[0] = qaParts[0].split()
            qaParts[0] = " ".join(qaParts[0][1:])

            if len(qaParts) == 1:
                print(qaParts)
                continue

            lineToWrite = previousA + ' <S> ' + qaParts[0]
            f_target.write(lineToWrite + '\n')

            lineToWrite = qaParts[0] + ' <S> ' + qaParts[1]
            f_target.write(lineToWrite + '\n')

            previousA = qaParts[1]

makePairs()