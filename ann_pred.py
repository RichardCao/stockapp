#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import MySQLdb
import datetime
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


class AnnPred(object):

    def __init__(self, size):
        self.conn = MySQLdb.connect(host="localhost",
                     user="stock",
                     passwd="stock",
                     db="stock",
                     charset="utf8")
        self.cursor = self.conn.cursor()
        self.size = size

    def get_index(self, date_f):
        sql_cmd = "SELECT close FROM sh50 where date='%s'" % date_f
        self.cursor.execute(sql_cmd)
        results = self.cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return None

    def prepare_date(self, start, end):
        self.stock_index = []
        t = start
        l_count = 0
        while t <= end:
            index = self.get_index(t)
            if index:
                if l_count != 0:
                    for p in xrange(1, l_count + 1):
                        self.stock_index.append(self.stock_index[-p] + (index - self.stock_index[-p]) / (l_count + 1) * p)
                    l_count = 0
                self.stock_index.append(index)
            else:
                l_count += 1
            t += datetime.timedelta(1)
        self.stock_unit = []
        max_p = max(self.stock_index)
        min_p = min(self.stock_index)
        delta = max_p - min_p
        self.stock_unit = [(item - min_p) / delta for item in self.stock_index]
        self.ds = SupervisedDataSet(8, 1)
        self.train_count = len(self.stock_unit) * 2 / 3 - 8
        for i in xrange(0, self.train_count):
            self.ds.addSample((self.stock_unit[i],
                               self.stock_unit[i + 1],
                               self.stock_unit[i + 2],
                               self.stock_unit[i + 3],
                               self.stock_unit[i + 4],
                               self.stock_unit[i + 5],
                               self.stock_unit[i + 6],
                               self.stock_unit[i + 7]),
                              (self.stock_unit[i + 8] - self.stock_unit[i + 7]))
    def train(self):
        self.trainer = BackpropTrainer(self.ann, self.ds)
        for i in xrange(0, 500):
            self.trainer.trainEpochs(1)
            print i
#        self.trainer.trainUntilConvergence()

    def test(self):
        self.right = 0
        self.wrong = 0
        for i in xrange(self.train_count, len(self.stock_unit) - 8):
            output = self.ann.activate((self.stock_unit[i],
                                        self.stock_unit[i + 1],
                                        self.stock_unit[i + 2],
                                        self.stock_unit[i + 3],
                                        self.stock_unit[i + 4],
                                        self.stock_unit[i + 5],
                                        self.stock_unit[i + 6],
                                        self.stock_unit[i + 7]))
            if output * (self.stock_unit[i + 8] - self.stock_unit[i + 7]) > 0:
                self.right += 1
            else:
                self.wrong +=1

    def buildAnn(self):
        self.ann = buildNetwork(*self.size, bias=True, hiddenclass=TanhLayer)

    def run(self):
        ann = AnnPred([8, 20, 20, 1])
        start = datetime.date(2014, 9, 1)
        end = datetime.date(2014, 9, 10)
        ann.prepare_date(start, end)
        ann.buildAnn()
        ann.train()
        ann.test()
        print ann.right
        print ann.wrong