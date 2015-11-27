#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]

import MySQLdb
from emotion import *

class SqlUtils(object):

    def __init__(self):
        self.conn=MySQLdb.connect(host="localhost",
                             user="stock",
                             passwd="stock",
                             db="stock",
                             charset="utf8")
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * from sh50")
        ret = self.cursor.fetchall()
        self.codelist = []
        for ins in ret:
            self.codelist.append(ins[1])

    def getEmotion(self, code, date_f):
        sql_cmd = "SELECT title, content, comment FROM pagedata where code=%s and date='%s'" % (code, date_f)
        print sql_cmd
        self.cursor.execute(sql_cmd)
        results = self.cursor.fetchall()
        if results:
            return sum([emotion_l(item) for item in results])
        else:
            return 0.0

if __name__ == '__main__':
    ins = SqlUtils()
    print ins.getEmotion('600000', '2015-02-07')
    print ins.getEmotion('600000', '2015-02-08')
    print ins.getEmotion('600000', '2015-02-09')
    print ins.getEmotion('600000', '2015-02-10')
    print ins.getEmotion('600000', '2015-02-11')
    print ins.getEmotion('600000', '2015-02-12')