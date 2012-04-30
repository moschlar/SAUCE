#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add new users by CSV file

@author: moschlar
"""

import os, sys, csv
from argparse import ArgumentParser

from sqlalchemy.exc import SQLAlchemyError

from paste.deploy import appconfig
from tg import config
from sauce.config.environment import load_environment
from sauce import model
from sauce.model import DBSession as Session
from sauce.lib.mail import sendmail

import transaction

def load_config(filename):
    conf = appconfig('config:' + os.path.abspath(filename))
    load_environment(conf.global_conf, conf.local_conf)

def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("conf_file", help="configuration to use")
    parser.add_argument("event_url", help="url of the event to use")
    parser.add_argument("csv_file", help="csv file to parse")
    return parser.parse_args()


URL = 'https://sauce.zdv.uni-mainz.de/'
ABOUT_URL = URL + 'about/'
PASSWORD_LENGTH = 8
fieldnames = ['i', 'matrikelnummer', 'last_name', 'first_name', 'pruefungsordnung', 'modul', 'email', 'nebenfach', 'studiengang', 'j']

def send_registration_mail(d, event):
    mail_text = u'''
Hallo %s %s,

du bist für die Veranstaltung %s im 
System for AUtomated Code Evaluation (SAUCE) angemeldet.

Dein Passwort lautet: %s

Du erreichst SAUCE unter: %s

Eine (deutschsprachige) Kurzeinführung in das System findest du auf 
der About-Seite: %s

Mit freundlichen Grüßen
i.A. Moritz Schlarb
''' % (d['first_name'].decode('utf-8'), d['last_name'].decode('utf-8'), event.name,
       d['password'], URL, ABOUT_URL)
    
    sendmail(d['email'], u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text)
    #sendmail('moschlar@students.uni-mainz.de', u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text)

def main():
    args = parse_args()
    load_config(args.conf_file)
    
    event = model.Event.by_url(args.event_url)
    
    with open(args.csv_file) as f:
        ff = fieldnames[:]
        reader = csv.DictReader(f, fieldnames=ff, delimiter=';')
        dicts = list(reader)
    
    for d in dicts:
        d['zdvuser'] = d['email'].split('@', 1)[0]
        #print d
        s = model.Student(user_name=d['zdvuser'], email_address=d['email'],
                          display_name=d['first_name'].decode('utf-8') + u' ' + d['last_name'].decode('utf-8'))
        #print s
        d['password'] = s.generate_password(PASSWORD_LENGTH)
        print d
        try:
            model.DBSession.add(s)
            model.DBSession.flush()
        except SQLAlchemyError as e:
            model.DBSession.rollback()
            raise e
        send_registration_mail(d, event)
    
    try:
        transaction.commit()
    except SQLAlchemyError as e:
        transaction.abort()
        raise e
    
    csv_out_file = args.csv_file.replace('.csv', '', 1) + '_out.csv'
    
    with open(csv_out_file, 'w') as f:
        ff = fieldnames[:]
        ff.append('zdvuser')
        ff.append('password')
        print ff
        w = csv.DictWriter(f, fieldnames=ff, delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(dicts)
    

if __name__ == '__main__':
    sys.exit(main())