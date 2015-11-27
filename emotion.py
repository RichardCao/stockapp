#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import sys
import jieba
word_weight = {}

reload(sys)
sys.setdefaultencoding('utf-8')

with open('/Users/Richard/PycharmProjects/QtStock/Stock//Res/key_weight.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        seg = line.split()
        if len(seg) == 3:
            word_weight[seg[0].encode('utf-8')] = float(seg[2])

def emotion_s(sentence):
    if not sentence:
        return 0.0
    if sentence.startswith('****'):
        return sum([word_weight.get(word.encode('utf-8'), 0.0) for word in jieba.cut(sentence[4:], cut_all=True)])
    elif sentence.startswith('####'):
        return sum([sum([word_weight.get(word.encode('utf-8'), 0.0) for word in jieba.cut(r)]) for r in sentence.split('####')])
    else:
        return sum([word_weight.get(word.encode('utf-8'), 0.0) for word in jieba.cut(sentence, cut_all=True)])

def emotion_l(data):
    if not data:
        return 0.0
    if len(data) == 3 and (isinstance(data, tuple) or isinstance(data, list)):
        return emotion_s(data[0]) + emotion_s(data[1]) / 5 + emotion_s(data[2]) / 25

if __name__ == '__main__':

    print emotion_s('涨,上涨,涨停')
    print emotion_s('####涨,上涨,涨停')
    print emotion_s('****涨,上涨,涨停')
    print 'aaa'
    print word_weight['涨']
    print 'bbb'
    print word_weight['涨'.encode('utf-8')]
    print 'ccc'
    print word_weight[u'涨'.encode('utf-8')]
    print 'ddd'
