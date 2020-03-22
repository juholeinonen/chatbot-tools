#!/usr/bin/env python3
# coding: utf-8

import csv
import argparse
import itertools
import random

parser = argparse.ArgumentParser(description="Creating pairs of users and their channels for the chat experiment")
parser.add_argument('csv_file', type=str, help="The csv file of the users and their passwords")
parser.add_argument('how_many', type=int, help="How many people chatting")
args = parser.parse_args()

usersPasswords = []
with open(args.csv_file, "r", encoding="utf-8") as fin:
    reader = csv.reader(fin)
    usersPasswords = [rows for rows in reader]

chattersChannels = []
result = None
while result is None:
    chattersChannels = []
    notChattedWithYet = [set([i for i in range(1, args.how_many + 1)]) for x in range(args.how_many)]
    try:
        channel = 1
        for chatRound in range(3):
            availableThisRound = set([i for i in range(1, args.how_many + 1)])
            for chat in range(args.how_many // 2):
                chatter1 = random.sample(availableThisRound, 1)[0]
                availableThisRound.remove(chatter1)

                chatter2 = random.sample(availableThisRound.intersection(notChattedWithYet[chatter1 - 1]), 1)[0]

                notChattedWithYet[chatter1 - 1].remove(chatter2)
                notChattedWithYet[chatter2 - 1].remove(chatter1)
                availableThisRound.remove(chatter2)

                chattersChannels.append([(chatter1, chatter2), channel])
                channel += 1
        result = 1
    except:
        pass


with open("experiment_set_up.txt", "w", encoding='utf-8') as fout:
    for userNumber, userPassword in enumerate(usersPasswords):
        fout.write("käyttäjätunnus:\t" + userPassword[0] + "\n")
        fout.write("salasana:\t\t" + userPassword[1] + "\n")
        chatNumber = 0
        chatText = ["ensimmäinen kanava:\t", "toinen kanava:\t\t", "kolmas kanava:\t\t"]
        for chatterChannel in chattersChannels:
            if userNumber+1 in chatterChannel[0]:
                if chatterChannel[1] < 10:
                    fout.write(chatText[chatNumber] + "0" + str(chatterChannel[1]) + "kanava\n")
                else:
                    fout.write(chatText[chatNumber] + str(chatterChannel[1]) + "kanava\n")
                chatNumber += 1
        fout.write("-------------------------------------------------\n")
    fout.write(str(chattersChannels))
