#!/usr/bin/env python3
# coding: utf-8

# import libraries
import re
import os
import sys
import argparse
import morfessor


parser = argparse.ArgumentParser(description='Preparing corpus for Transformer Language Model')
parser.add_argument('--split_type', type=str, default='word',
                    choices=['word', '+morf+', '+char+', 'char'],
                    help='How to split the corpus')
parser.add_argument('dataset', type=str,
                    help='The dataset to prepare')
parser.add_argument('--morfessor_model', type=str,
                    help='The morfessor model')
args = parser.parse_args()

if args.split_type == '+morf+':
    if args.morfessor_model is None:
        parser.error("option +morphs+ requires a matching Morfessor model.")
    else:
        morfessorIO = morfessor.MorfessorIO()
        MorfessorModel = morfessorIO.read_binary_model_file(args.morfessor_model)


def splitText(line):
    if args.split_type == '+char+':
        sentenceAsCharacters = []
        words = line.split()
        for word in words:
            if len(word) == 1:
                sentenceAsCharacters.append(word)
            else:
                sentenceAsCharacters.append(word[0] + "+")
                for letter in word[1:-1]:
                    sentenceAsCharacters.append("+" + letter + "+")
                sentenceAsCharacters.append("+" + word[-1])
        line = " ".join(sentenceAsCharacters)

    elif args.split_type == '+morf+':
        sentenceAsMorfs = []
        words = line.split()
        for word in words:
            morfs, _ = MorfessorModel.viterbi_segment(word)
            if len(morfs) == 1:
                sentenceAsMorfs.append(morfs[0])
            else:
                sentenceAsMorfs.append(morfs[0] + "+")
                for morf in morfs[1:-1]:
                    sentenceAsMorfs.append("+" + morf + "+")
                sentenceAsMorfs.append("+" + morfs[-1])
        line = " ".join(sentenceAsMorfs)
    return line


def cleanText():
    trainFileName, file_ext = os.path.splitext(args.dataset)

    if args.split_type == '+char+':
        varyingFileName = "pCharp"
    elif args.split_type == '+morf+':
        varyingFileName = "pMorfp"
    else:
        varyingFileName = "ERROR"

    cleanedFileName = trainFileName + "_cleaned" + varyingFileName + file_ext

    with open(args.dataset, 'r', encoding='utf-8') as f_source,\
            open(cleanedFileName, 'w', encoding='utf-8') as f_target:
        for line in f_source:
            line_parts = line.split(' ', maxsplit=1)
            line = line_parts[1]
            line = line.lower()
            # I Don't remember what this does.. removes certain characters?
            line = re.sub("[^a-zA-Z\x7f-\xff]", " ", line)
            line = re.sub(" +", " ", line)
            line = line.strip()
            if len(line) == 0:
                line = "<UNK>"
                f_target.write(line_parts[0] + ',' + line + "\n")
                continue

            line = splitText(line)

            f_target.write(line_parts[0] + ',' + line + "\n")

cleanText()
