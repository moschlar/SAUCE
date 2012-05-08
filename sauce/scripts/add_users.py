#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add new users by CSV file

@author: moschlar
"""

import os, sys, csv, time
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
    parser.add_argument("csv_fields", default='firstrow', nargs='?',
                        help="csv field names, comma separated - field names that match a database field get used")
    return parser.parse_args()


URL = 'https://sauce.zdv.uni-mainz.de/'
DOCS_URL = URL + 'docs/deutsch'
PASSWORD_LENGTH = 8

def send_registration_mail(d, event):
    mail_text = u'''
Hallo %s,

du bist für die Veranstaltung %s im 
System for AUtomated Code Evaluation (SAUCE) angemeldet.

Dein Benutzername lautet: %s
Dein Passwort lautet: %s
(Du kannst und solltest dein Passwort in deinen Profileinstellungen
ändern.)

Du erreichst SAUCE unter: %s

Eine (deutschsprachige) Kurzeinführung in das System findest du
unter: %s

Falls du Fehler in den Aufgaben oder im System feststellst, Schwierigkeiten
bei der Bedienung hast, oder Verbesserungsvorschläge, melde
diese bitte per eMail an moschlar@students.uni-mainz.de.

Mit freundlichen Grüßen
i.A. Moritz Schlarb
''' % (d['display_name'].decode('utf-8'), event.name, d['user_name'], d['password'], URL, DOCS_URL)
    
    print mail_text
    
    sendmail(d['email_address'], u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text)
    #sendmail('moschlar@students.uni-mainz.de', u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text)

def main():
    args = parse_args()
    load_config(args.conf_file)
    
    #event = model.Event.by_url(args.event_url)
    
    if args.csv_fields == 'firstrow':
        fields = None
    else:
        fields = args.csv_fields
    
    with open(args.csv_file) as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter=';')
        dicts = list(reader)
    
    errors = []
    
    for d in dicts:
        event = model.Event.by_url(args.event_url)
        print d
        s = model.Student(user_name=d['user_name'], display_name=d['display_name'].decode('utf-8'),
                          email_address=d['email_address'])
        try:
            s._lessons.append(model.Lesson.by_lesson_id(d['lesson_id'], event))
        except Exception as e:
            print e.message
            errors.append((e, d))
        #print s
        d['password'] = s.generate_password(PASSWORD_LENGTH)
        print d
        try:
            model.DBSession.add(s)
            #model.DBSession.flush()
            transaction.commit()
        except SQLAlchemyError as e:
            #model.DBSession.rollback()
            transaction.abort()
            print e.message
            errors.append((e, s))
            #raise e
        else:
            send_registration_mail(d, event)
            time.sleep(30)
    
#    try:
#        transaction.commit()
#    except SQLAlchemyError as e:
#        transaction.abort()
#        raise e
    
    csv_out_file = args.csv_file.replace('.csv', '', 1) + '_out.csv'
    
    with open(csv_out_file, 'w') as f:
        if fields:
            fields.append('password')
        w = csv.DictWriter(f, fieldnames=dicts[0].keys(), delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(dicts)
    
    print errors

if __name__ == '__main__':
    sys.exit(main())