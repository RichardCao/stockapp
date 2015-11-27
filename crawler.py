#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright(C) 2015 [Ruichaung Cao]


import requests
from bs4 import BeautifulSoup
import bs4

def gettitle(code, url):
    ret = []
    page = requests.get(url)
    page.encoding = 'gb2312'
    ori_data = page.text
    data = BeautifulSoup(ori_data, 'html.parser')
    tr_list = data.find_all('table')[1].tbody.find_all('tr')
    for tr in tr_list:
        try:
            td = tr.find_all('td')
            if  td[2].a.string.strip() == '新浪股吧最新版规':
                continue
            date_f = td[4].string.strip()
            if u'分钟前' in date_f or u'今天' in date_f:
                date_f = '09-16'
            else:
                date_f = date_f.replace(u'月', '-')
                date_f = date_f.replace(u'日', '')
            if 'linkblack' in td[2].a['class'] and 'f14' in td[2].a['class']:
                ret.append(' '.join([code, date_f, td[2].a.string.strip(), 'http://guba.sina.com.cn/%s' % td[2].a['href'].strip(), td[0].string.strip(), td[1].string.strip()]))
        except:
            pass
    return ret

def getpage(info, content):
    ret = []
    ori_data = None
    if info:
        i_list = info.split()
        url = i_list[-3]
        page = requests.get(url)
        page.encoding = 'gb2312'
        ori_data = page.text
        if u'本帖已删除,或访问受限' in page.text:
            return ret
    else:
        ori_data = content

    data = BeautifulSoup(ori_data, 'html.parser')
    time_t = data.find_all(attrs={'class': 'fl_left iltp_time'})[0].string.split()[0]
    time_t = time_t.replace('月', '-')
    time_t = time_t.replace('日', '')
    if '年' in time_t:
        time_t = time_t.replace(u'年', '-')
    else:
        time_t = u'2015-' + time_t
    i_list[1] = time_t
    ret.append(' '.join(i_list))

    div_list = data.find_all(attrs={'class': 'ilt_p'})
    cont_l = []
    for p in div_list[0].contents:
        if isinstance(p, bs4.element.Tag):
            for q in p.children:
                if isinstance(q, bs4.element.Tag):
                    for r in q.children:
                        if isinstance(r, bs4.element.Tag):
                            for s in r.children:
                                if s.string and s.string.strip() and s.string != r.string and not 'table' in s.string:
                                        cont_l.append(s.string)
                        elif r.string and r.string.strip() and not 'table' in r.string:
                            cont_l.append(r.string)
                elif q.string and q.string.strip() and not 'table' in q.string:
                    cont_l.append(p.string)
        elif p.string and p.string.strip() and not 'table' in p.string:
            cont_l.append(p.string)
    ret.append('****' + ' '.join([c for c in cont_l if c]).replace('\n', ' '))

    comm_l = []
    for item in div_list[1:]:
        if item.string:
            comm_l.append(item.string)
    ret.append('####' + '####'.join([c for c in comm_l if c]).replace('\n', ' '))
    return ret
