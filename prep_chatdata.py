#!/usr/bin/env python3
# coding: utf-8

# import libraries
import re
import os
import sys
import argparse
import morfessor

def parse_arguments():
    parser = argparse.ArgumentParser(description='Preparing corpus for Transformer Language Model')
    parser.add_argument('--split_type', type=str, default='word',
                        choices=['word', '+morf+', '+char+', 'char'],
                        help='How to split the corpus')
    parser.add_argument('dataset', type=str,
                        help='The dataset to prepare')
    parser.add_argument('--morfessor_model', type=str,
                        help='The morfessor model')
    parser.add_argument('--clean_string', action='store_true',
                        help='Lowers text, uses regex command to clean.')
    parser.add_argument('--chat_format', type=str, default='convai2',
                        choices=['convai2'],
                        help='In which format is the chat saved to text.')
    args = parser.parse_args()

    morfessor_binary = None
    if args.split_type == '+morf+':
        if args.morfessor_model is None:
            parser.error("option +morphs+ requires a matching Morfessor model.")
        else:
            morfessorIO = morfessor.MorfessorIO()
            morfessor_binary = morfessorIO.read_binary_model_file(args.morfessor_model)

    return args, morfessor_binary 


def split_text(line, split_type, morfessor_binary):
    if split_type == '+char+':
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

    elif split_type == '+morf+':
        sentenceAsMorfs = []
        words = line.split()
        for word in words:
            morfs, _ = morfessor_binary.viterbi_segment(word)
            if len(morfs) == 1:
                sentenceAsMorfs.append(morfs[0])
            else:
                sentenceAsMorfs.append(morfs[0] + "+")
                for morf in morfs[1:-1]:
                    sentenceAsMorfs.append("+" + morf + "+")
                sentenceAsMorfs.append("+" + morfs[-1])
        line = " ".join(sentenceAsMorfs)
    return line


def prepare_chat(arguments, morfessor_binary):
    trainFileName, file_ext = os.path.splitext(arguments.dataset)

    if arguments.split_type == '+char+':
        varyingFileName = "pCharp"
    elif arguments.split_type == '+morf+':
        varyingFileName = "pMorfp"
    else:
        varyingFileName = "ERROR"

    cleanedFileName = trainFileName + "_cleaned" + varyingFileName + file_ext

    with open(arguments.dataset, 'r', encoding='utf-8') as f_source,\
        open(cleanedFileName, 'w', encoding='utf-8') as f_target:
        for line in f_source:
            if arguments.chat_format == "convai2":
                # Splits the number of Q/A and the text itself
                line_parts = line.split(' ', maxsplit=1)
                dialog_round_number =   line_parts[0]
                dialog_round_text   =   line_parts[1]

                dialog_round_in_subwords = []

                dialog_turns = dialog_round_text.split('\t', maxsplit=1) # does not work now if sentence_part has the false choices
            else:
                # placeholder, currently everything should be convai2
                dialog_turns = line.split()

            for dialog_turn in dialog_turns:
                if arguments.clean_string:
                    dialog_turn = dialog_turn.lower()
                    # I Don't remember what this does.. removes certain characters?
                    dialog_turn = re.sub("[^a-zA-Z\x7f-\xff]", " ", dialog_turn)
                    dialog_turn = re.sub(" +", " ", dialog_turn)

                dialog_turn = dialog_turn.strip()
                if len(dialog_turn) == 0:
                    dialog_round_in_subwords.append('<UNK>')
                else:
                    dialog_round_in_subwords.append(split_text(dialog_turn, arguments.split_type, morfessor_binary))

            dialog_to_write = "\t".join(dialog_round_in_subwords)
            f_target.write(dialog_round_number + ' ' + dialog_to_write + '\n')


def main(arguments, morfessor_binary):
    prepare_chat(arguments, morfessor_binary)


if __name__ == '__main__':
    arguments, morfessor_binary = parse_arguments()
    main(arguments, morfessor_binary)
