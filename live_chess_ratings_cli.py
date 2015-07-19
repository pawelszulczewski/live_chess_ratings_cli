#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# takes live chess ratings from http://www.2700chess.com
# and prints in command-line
#
# GPLv2
# psz, pawel <at> szulczewski <dot> org, march 2015

import urllib2
import texttable
from bs4 import BeautifulSoup
from sys import exit

table_header = ["No", "↑↓", "Surname", "Country", "ELO", "ELO +-"]
data = []

try :
    final_table = texttable.Texttable()
    final_table.add_row(table_header)
    
    web_page = urllib2.urlopen("http://2700chess.com").read()
    soup = BeautifulSoup(web_page, "lxml")
    table = soup.find('table', {'id': 'live-ratings-table'})
    rows = table.find_all('tr')
    
    for row in rows:
       cols = row.find_all('td')
       cols = [ele.text.strip() for ele in cols]
       data.append([ele for ele in cols])

    for players in data:
        d = []
        for pl_data in players[0:6]:
            if pl_data:
                d.append(pl_data.splitlines()[0].encode('UTF8'))
            else:
                d.append("-")
        if (len(d) == 6):
            final_table.add_row(d)

    print final_table.draw()
except urllib2.HTTPError :
        print("HTTPERROR!")
        exit(1)
except urllib2.URLError :
        print("URLERROR!")
        exit(2)
        
exit(0)
