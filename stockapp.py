#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import sys
import random
import datetime
import pylab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ann_pred import AnnPred
from crawlwin import CrawlWin
from sql_utils import SqlUtils
from ann_pred import *

class mainUI(QGraphicsView):
    def __init__(self, parent=None):
        super(mainUI, self).__init__(parent)
        self.resize(1200, 600)
        self.move(200, 200)

        self.hbox = QtGui.QHBoxLayout()
        self.hbox_lh = QtGui.QHBoxLayout()
        self.hbox_ll = QtGui.QHBoxLayout()
        self.hbox_rh = QtGui.QHBoxLayout()
        self.hbox_rl = QtGui.QHBoxLayout()
        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox2 = QtGui.QVBoxLayout()

        self.label_f = QtGui.QLabel("From")
        self.label_t = QtGui.QLabel("To")
        self.from_l_d = QtGui.QLineEdit('20140701')
        self.to_l_d = QtGui.QLineEdit('20140801')
        self.hbox_lh.addWidget(self.label_f)
        self.hbox_lh.addWidget(self.from_l_d)
        self.hbox_lh.addWidget(self.label_t)
        self.hbox_lh.addWidget(self.to_l_d)

        self.label_r_f = QtGui.QLabel("From")
        self.label_r_t = QtGui.QLabel("To")
        self.from_r_d = QtGui.QLineEdit('20140801')
        self.to_r_d = QtGui.QLineEdit('2014091')
        self.hbox_rh.addWidget(self.label_r_f)
        self.hbox_rh.addWidget(self.from_r_d)
        self.hbox_rh.addWidget(self.label_r_t)
        self.hbox_rh.addWidget(self.to_r_d)

        self.figure_l = plt.figure()
        self.canvas_l = FigureCanvas(self.figure_l)
        self.button_load = QtGui.QPushButton('Load Data')
        self.button_load.clicked.connect(self.load)

        self.figure_r = plt.figure()
        self.canvas_r = FigureCanvas(self.figure_r)
        self.button_predict = QtGui.QPushButton('Predict Price')
        self.button_predict.clicked.connect(self.predict)

        self.radio_hbox = QtGui.QHBoxLayout()
        self.check_hbox = QtGui.QHBoxLayout()
        self.radio1 = QtGui.QRadioButton('Show Value')
        self.radio1.setChecked(True)
        self.radio2 = QtGui.QRadioButton('Show Change')
        self.radio1.clicked.connect(self.radioclicked)
        self.radio2.clicked.connect(self.radioclicked)
        self.check1 = QtGui.QCheckBox('News')
        self.check1.setCheckable(False)
        self.check2 = QtGui.QCheckBox('Weibo')
        self.check3 = QtGui.QCheckBox('Price')
        self.check1.clicked.connect(self.checkclicked)
        self.check2.clicked.connect(self.checkclicked)
        self.check3.clicked.connect(self.checkclicked)
        self.check_hbox.addWidget(self.check1)
        self.check_hbox.addWidget(self.check2)
        self.check_hbox.addWidget(self.check3)
        self.radio_hbox.addWidget(self.radio1)
        self.radio_hbox.addWidget(self.radio2)
        self.hbox_ll.addLayout(self.check_hbox)
        self.hbox_ll.addLayout(self.radio_hbox)

        self.radio1_r = QtGui.QRadioButton('Selected the Best')
        self.radio1_r.setChecked(True)
        self.radio2_r = QtGui.QRadioButton('Take a Vote')
        self.radio1_r.clicked.connect(self.result_type)
        self.radio2_r.clicked.connect(self.result_type)
        self.hbox_rl.addWidget(self.radio1_r)
        self.hbox_rl.addWidget(self.radio2_r)

        self.vbox1.addLayout(self.hbox_lh)
        self.vbox1.addWidget(self.canvas_l)
        self.vbox1.addLayout(self.hbox_ll)
        self.vbox1.addWidget(self.button_load)
        self.vbox2.addLayout(self.hbox_rh)
        self.vbox2.addWidget(self.canvas_r)
        self.vbox2.addLayout(self.hbox_rl)
        self.vbox2.addWidget(self.button_predict)
        self.hbox.addLayout(self.vbox1)
        self.hbox.addLayout(self.vbox2)

        self.box = QtGui.QVBoxLayout()
        self.box.addLayout(self.hbox)
        self.label_status = QtGui.QLabel("Ready")
        self.box.addWidget(self.label_status)

        self.setLayout(self.box)

        self.sql = SqlUtils()

        self.setWindowTitle('Stock Prediction')

    def load(self):
        print 'load'

        start = str(self.from_l_d.text())
        end = str(self.to_l_d.text())
        start_t = datetime.datetime.strptime(start,'%Y%m%d').date()
        end_t = datetime.datetime.strptime(end,'%Y%m%d').date()
        cur = start_t
        print cur
        self.emotion = []
        cnt = 0
        while cur < end_t:
            print cur
            self.emotion.append(self.sql.getEmotion('600000', cur))
            cnt += 1
            cur += datetime.timedelta(1)

        data1 = [random.random() * 70 - 30 for i in range(cnt)]
        data2 = [random.random() * 80 - 40 for i in range(cnt)]
        data3 = [random.random() * 90 - 50 for i in range(cnt)]

        print self.emotion

        ax = self.figure_l.add_subplot(111)
        ax.clear()
        ax.hold(True)
        if self.check1.isChecked():
            ax.plot(data1, 'rd-')
        if self.check2.isChecked():
            ax.plot(self.emotion, 'gd-')
        if self.check3.isChecked():
            ax.plot(data3, 'bD-')


#        data2 = [random.random() for i in range(100)]
#        ax2 = self.figure_r.add_subplot(111)
#        ax2.hold(False)
#        ax2.plot(data2, '*-')

        self.canvas_l.draw()

    def predict(self):
        print 'predict'
        self.label_status.setText("predict")
        start = str(self.from_r_d.text())
        end = str(self.to_r_d.text())
        start_t = datetime.datetime.strptime(start,'%Y%m%d').date()
        end_t = datetime.datetime.strptime(end,'%Y%m%d').date()

        ann = AnnPred([8,20,20,1])
        ann.prepare_date(start_t, end_t)
        ann.buildAnn()
        ann.train()
        ann.test()

        cur = start_t
        cnt = 0
        while cur < end_t:
            cur += datetime.timedelta(1)
            cnt += 1
        data1 = [random.random() * 2 - 1 for i in range(cnt)]
        ax = self.figure_r.add_subplot(111)
        ax.clear()
        ax.hold(True)
        ax.plot(data1, 'rd-')
        self.canvas_r.draw()

    def radioclicked(self):
        print 'radio clicked'

    def checkclicked(self):
        print 'check clicked'

    def result_type(self):
        print 'result type'
        self.subwin()

    def subwin(self):
        subw = CrawlWin(parent=self)
        subw.show()

    def test(self):
        print 'test'

if __name__ == "__main__":
#    x = range(10)
#    y = [random.randint(1,10) for i in xrange(10)]
#    b = pylab.plot(x, y)
#    print b

#    pylab.randn(2,3)
#    np.random.randn(2,3)
#    plt.hist([1,1,1,2,3,3])

    app = QApplication(sys.argv)
    w = mainUI()
    w.show()
    sys.exit(app.exec_())

