#!/usr/bin/env python3
# coding: utf-8

# This code is based on this thread and comment:
# https://github.com/kimiyoung/transformer-xl/issues/49#issuecomment-471790537

# import libraries
import re
import morfessor

import torch
import torch.nn.functional as F
import numpy as np

from mem_transformer import MemTransformerLM
from data_utils import get_lm_corpus


MODEL_FP = "2h_QA_transformer/model.pt"

USE_CUDA = False
BATCH_SIZE = 1
TGT_LEN = 1
EXT_LEN = 0
MEM_LEN = 2000
CLAMP_LEN = 1000
GEN_LEN = 40
SAME_LENGTH = True


morfessorIO = morfessor.MorfessorIO()
MorfessorModel = morfessorIO.read_binary_model_file("models/model.bin")

corpus = get_lm_corpus("data", "Ctrain")

def parseUserInput(line):

    line = line.lower()
    # I Don't remember what this does.. removes certain characters?
    line = re.sub("[^a-zA-Z\x7f-\xff]", " ", line)
    line = re.sub(" +", " ", line)
    line = line.strip()

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


device = torch.device("cuda" if USE_CUDA else "cpu")

# Load the best saved model
with open(MODEL_FP, 'rb') as f:
    model = torch.load(f, map_location='cpu')
model.backward_compatible()
model = model.to(device)

# Make sure model uses vanilla softmax
if model.sample_softmax > 0:
    raise NotImplementedError()
if model.crit.n_clusters != 0:
    raise NotImplementedError()

# Change training length/memory attrs
model.reset_length(TGT_LEN, EXT_LEN, MEM_LEN)
if CLAMP_LEN > 0:
    model.clamp_len = CLAMP_LEN
if SAME_LENGTH:
    model.same_length = True

# Turn on evaluation mode which disables dropout.
model.eval()


# Generate sequences of specified length and number
with torch.no_grad():

    # Initialize state
    prev_token = torch.zeros([TGT_LEN, BATCH_SIZE], dtype=torch.int64).to(device)
    mems = tuple()

    while True:
        try:
            # Create buffer for generated sequences
            samples = torch.zeros([0, BATCH_SIZE], dtype=torch.int64).to(device)

            userMessage = input(":")
            parsedUserMessage = parseUserInput(userMessage)

            idxToBot = []
            for morf in parsedUserMessage.split():
                idxToBot.append(corpus.vocab.sym2idx[morf])
            idxToBot.append(corpus.vocab.sym2idx['<S>'])

            for idx in idxToBot:
                ret = model.forward_generate(prev_token, *mems)

                # Retrieve logits and memory
                logits, mems = ret[0], ret[1:]

                token = torch.tensor([[idx]], dtype=torch.int64).to(device)

                # Add new token to buffer and update history
                prev_token = token

            token = ""
            # Autoregressive sampling
            while token != corpus.vocab.sym2idx['<S>']:
                ret = model.forward_generate(prev_token, *mems)

                # Retrieve logits and memory
                logits, mems = ret[0], ret[1:]

                # Compute probabilities
                probs = F.softmax(logits, dim=-1)

                # Sample from probabilities
                sampler = torch.distributions.categorical.Categorical(probs=probs)
                token = sampler.sample()

                # Add new token to buffer and update history
                samples = torch.cat([samples, token], dim=0)
                prev_token = token

            generatedTextList = []
            for sample in samples:
                generatedTextList.append(corpus.vocab.idx2sym[sample])
            generatedTextString = " ".join(generatedTextList)
            CleanedGeneratedTextString = generatedTextString.replace("+ +","").replace(" +", "").replace("+ ", "")
            print(CleanedGeneratedTextString)

        except KeyboardInterrupt:
            print('-' * 10)
            print('Exiting from chat early')
