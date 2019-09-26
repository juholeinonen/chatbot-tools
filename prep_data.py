#!/usr/bin/env python3
# coding: utf-8

# import libraries
import re
import os
import sys


def cleanText(trainFile):
    toChars = True
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

def main(trainFile):
    cleanText(trainFile)

if __name__ == '__main__':
    main(sys.argv[1])