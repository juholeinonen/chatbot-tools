#!/usr/bin/env python3
# coding: utf-8

# import libraries
import os
import argparse

parser = argparse.ArgumentParser(description='Preparing corpus for Transformer Language Model')
parser.add_argument('dataset', type=str,
                    help='The dataset to prepare')
parser.add_argument('--num_replies', type=int, help='How many replies for a datapoint', default=5)

args = parser.parse_args()

def makePairs():
    trainFileName, file_ext = os.path.splitext(args.dataset)

    qaFileName = trainFileName + "_varQA" + file_ext

    with open(args.dataset, 'r', encoding='utf-8') as f_source, \
            open(qaFileName, 'w', encoding='utf-8') as f_target:

        first_of_new_chat = True
        previousA = "moi mitä kuuluu"
        chatters = {}
        history = []

        for line in f_source:
            chatter, text = line.split(',', maxsplit=1)
            if chatter not in chatters and len(chatters) == 2 or len(chatters) == 0:
                chatters = {chatter}
                history = []
                history.append(previousA)
                history.append(text.strip())

            elif chatter not in chatters and len(chatters) == 1:
                chatters.add(chatter)
                history.append(text.strip())

            elif len(history) < args.num_replies:
                history.append(text.strip())

            else:
                del history[0]
                history.append(text.strip())

            lineToWrite = " <S> ".join(history)
            f_target.write(lineToWrite + '\n')


makePairs()