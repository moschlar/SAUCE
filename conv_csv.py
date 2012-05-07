#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add new users by CSV file

@author: moschlar
"""

import os, sys, csv

fieldnames_a = ['i', 'matrikelnummer', 'last_name', 'first_name',
              'pruefungsordnung', 'modul', 'email', 'nebenfach',
              'studiengang', 'j']
csv_file_a = '/home/moschlar/workspace/SAUCE/TeilnehmerEIP.csv'
fieldnames_b = ['matrikelnummer','last_name','first_name','gruppe','email']
csv_file_b = '/home/moschlar/workspace/SAUCE/Gruppen_eip.csv'

csv_file_out = '/home/moschlar/workspace/SAUCE/eip_out.csv'
fieldnames_out = ['user_name', 'display_name', 'email_address', 'lesson_id']

def main():
    
    with open(csv_file_a) as f:
        reader = csv.DictReader(f, fieldnames=fieldnames_a, delimiter=';')
        aa = list(reader)
    dict_a = dict((d['matrikelnummer'], d) for d in aa)
    set_a = set(dict_a.iterkeys())
    
    with open(csv_file_b) as f:
        f.readline()
        reader = csv.DictReader(f, fieldnames=fieldnames_b, delimiter=',')
        bb = list(reader)
    dict_b = dict((d['matrikelnummer'], d) for d in bb)
    set_b = set(dict_b.iterkeys())
    
    print 'Only in a:'
    for d in set_a - set_b:
        print dict_a[d]
#    print 'Only in b:'
#    for d in set_b - set_a:
#        print dict_b[d]
    
    studs = []
    
    for d in set_b:
        #stud_a = dict_a[d]
        stud_b = dict_b[d]
        stud = {}
        user_name = stud_b['email'].split('@', 1)[0]
        if '.' in user_name or '-' in user_name or '_' in user_name:
            print 'Invalid user_name: %s' % user_name
            user_name = raw_input('New user_name: ')
        stud['user_name'] = user_name
        stud['display_name'] = (stud_b['first_name'].decode('latin-1') + u' ' + stud_b['last_name'].decode('latin-1')).encode('utf-8')
        stud['email_address'] = stud_b['email']
        stud['lesson_id'] = stud_b['gruppe']
        print stud
        studs.append(stud)
    
    with open(csv_file_out, 'w') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames_out, delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(studs)
    

if __name__ == '__main__':
    sys.exit(main())