#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


key_weight = {}    # word, value
with open('./Res/key_weight.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        seg = line.split()
        if len(seg) == 3 and seg[2] != '0':
            key_weight[seg[0].encode('utf-8')] = float(seg[2]) / 3

print len(key_weight)
keyp = [key for key in key_weight if key_weight[key] < 0]
print len(keyp)

word_classify = {}
with open('./Res/cidian-utf8.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        seg = line.split()
        for word in seg[1:]:
            word_classify[word] = seg[0][:-2]
print len(word_classify)

def replace_word(word1, word2):
    if word_classify(word1) == word_classify(word2):
        return word1 if word1 < word2 else word2

data = {}       # date, entence

