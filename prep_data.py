#!/usr/bin/env python3
# coding: utf-8

# import libraries
import re
import os
import sys


parser = argparse.ArgumentParser(description='Preparing corpus for Transformer Language Model')
parser.add_argument('--split-type', type=str, default='word',
                    choices=['word', '+morph+', '+char+', 'char'],
                    help='How to split the corpus')
parser.add_argument('--dataset', type=str, default='train',
                    choices=['train', 'valid'],
                    help='dataset name')
args = parser.parse_args()


def cleanText():
    trainFileName, file_ext = os.path.splitext(trainFile)
    if toChars:
        cleanedFileName = trainFileName + "_cleanedChars" + file_ext
    else:
        cleanedFileName = trainFileName + "_cleaned" + file_ext

    with open(trainFile, 'r', encoding='utf-8') as f_source,\
            open(cleanedFileName, 'w', encoding='utf-8') as f_target:
        for line in f_source:
            line = line.lower()
            line = re.sub("[^a-zA-Z\x7f-\xff]", " ", line)
            line = re.sub(" +", " ", line)
            line = line.strip()

            if toChars:
                sentenceAsCharacters = []
                words = line.split()
                for word in words:
                    sentenceAsCharacters.append(word[0] + "+")
                    for letter in word[1:-1]:
                        sentenceAsCharacters.append("+" + letter + "+")
                    sentenceAsCharacters.append("+" + word[-1])
                line = " ".join(sentenceAsCharacters)


            f_target.write(line + "\n")

cleanText()