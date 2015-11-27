#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import sys
import random
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import requests

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from crawler import *

class CrawlWin(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CrawlWin, self).__init__(parent)
        self.resize(600, 300)
        self.move(200, 200)

        self.label_l = QtGui.QLabel('Original Data')
        self.area_l = QtGui.QPlainTextEdit()
        self.area_l.setReadOnly(True)
        url = "http://guba.sina.com.cn/?s=bar&name=sh%s&type=0&page=%d" % ('600000', 100)
        print url
        ret = requests.get(url)
        ret.encoding = 'gb2312'
        self.area_l.setPlainText(ret.text)

        self.label_r = QtGui.QLabel('Clean Data')
        self.area_r = QtGui.QPlainTextEdit()
        self.area_r.setReadOnly(True)

        contentdata = gettitle('600000', url)
        print contentdata
        self.area_r.setPlainText(contentdata[1] + '\n' + contentdata[2])

#        self.hbox = QtGui.QHBoxLayout()
#        self.hbox_lh = QtGui.QHBoxLayout()
#        self.hbox_ll = QtGui.QHBoxLayout()
#        self.hbox_rh = QtGui.QHBoxLayout()
#        self.hbox_rl = QtGui.QHBoxLayout()
        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox1.addWidget(self.label_l)
        self.vbox1.addWidget(self.area_l)
        self.vbox2 = QtGui.QVBoxLayout()
        self.vbox2.addWidget(self.label_r)
        self.vbox2.addWidget(self.area_r)


        self.box = QtGui.QHBoxLayout()
        self.box.addLayout(self.vbox1)
        self.box.addLayout(self.vbox2)

        self.setLayout(self.box)

        if parent:
            parent.test()
