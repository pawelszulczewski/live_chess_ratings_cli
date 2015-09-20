#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# takes live chess ratings from http://www.2700chess.com
# and prints in command-line
#
# GPLv2
# psz, pawel <at> szulczewski <dot> org, march-september 2015

import urllib2
import getopt
import sys
from bs4 import BeautifulSoup

data = []

def main (argv):
    try :    
        opts, args = getopt.getopt(argv,"tlg:")    
        for opt, arg in opts:
            if opt == '-t':
                table_output = True
                line_output  = None
            elif opt == '-l':
                table_output = None
                line_output = True
                
        web_page = urllib2.urlopen("http://2700chess.com").read()
        soup = BeautifulSoup(web_page, "lxml")            

        if table_output:
            import texttable
            table_header = ["No", "↑↓", "Surname", "Country", "ELO", "ELO +-"]            
            final_table = texttable.Texttable()
            final_table.add_row(table_header)
            
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
                if table_output:
                    final_table.add_row(d)
                else:
                    print ('\t'.join (map (str, d)))

        if table_output:
            print final_table.draw()
            
    except getopt.GetoptError:
          print 'live_chess_ratings_cli.py'
          print '\t\t -t\t output as a table'
          print '\t\t -l\t output as lines'
          exit(3)
    except urllib2.HTTPError :
        print("HTTPERROR!")
        exit(1)
    except urllib2.URLError :
        print("URLERROR!")
        exit(2)

if __name__ == "__main__":
       main(sys.argv[1:])
       exit(0)
