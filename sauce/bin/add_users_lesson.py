#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add new users by CSV file

@author: moschlar
"""
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, sys, csv, time
from argparse import ArgumentParser

from sqlalchemy.exc import SQLAlchemyError

from paste.deploy import appconfig
from tg import config
from sauce.config.environment import load_environment
from sauce import model
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


URL = u'https://sauce.zdv.uni-mainz.de/'
DOCS_URL = URL + u'docs/deutsch'
FROM_EMAIL = u'moschlar@students.uni-mainz.de'
FROM_NAME = u'i.A. Moritz Schlarb'
PASSWORD_LENGTH = 8


def send_registration_mail(s, d, event):
    mail_text = u'''
Hallo %s,

du bist für die Veranstaltung %s im
System for AUtomated Code Evaluation (SAUCE) angemeldet.

Du erreichst SAUCE unter: %s
''' % (s.display_name, event.name, URL)

    if 'password' in d:
        mail_text += u'''
Eine (deutschsprachige) Kurzeinführung in das System findest du
unter: %s

Dein Benutzername lautet: %s
Dein Passwort lautet: %s
(Du kannst und solltest dein Passwort in deinen Profileinstellungen
ändern.)
''' % (DOCS_URL, s.user_name, d['password'])
    else:
        mail_text += u'''
Dein Benutername lautet: %s
Dein Passwort wurde nicht geändert!
''' % (s.user_name)

    if 'lesson' in d:
        if d['lesson']:
            mail_text += u'''
Du bist registriert für: %s
''' % (d['lesson'].name)

    mail_text += u'''
Falls du Fehler in den Aufgaben oder im System feststellst, Schwierigkeiten
bei der Bedienung hast, oder Verbesserungsvorschläge, melde
diese bitte per eMail an %s.

Mit freundlichen Grüßen
%s
''' % (FROM_EMAIL, FROM_NAME)

    print mail_text

#     sendmail(u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text, s.email_address)
#     sendmail(u'[%s] Dein Passwort für SAUCE' % (event._url), mail_text, 'test@localhost')


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
        if d['lesson_id'] != 0:
            event = model.Event.by_url(args.event_url)
            print d
            s = model.User.query.filter_by(user_name=d['user_name']).first()
            if not s:
                s = model.User(user_name=d['user_name'],
                    last_name=d['last_name'].decode('utf-8'),
                    first_name=d['first_name'].decode('utf-8'),
                    email_address=d['email_address'])
                d['password'] = s.generate_password(PASSWORD_LENGTH)
            try:
                l = model.Lesson.by_lesson_id(d['lesson_id'], event)
                d['lesson'] = l
                s._lessons.append(l)
            except Exception as e:
                print e.message
                errors.append((e, d))
            #print s
            print d
            try:
                model.DBSession.add(s)
                send_registration_mail(s, d, event)
                #model.DBSession.flush()
                transaction.commit()
            except SQLAlchemyError as e:
                #model.DBSession.rollback()
                transaction.abort()
                print e.message
                errors.append((e, s))
                #raise e

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
    print >>sys.stderr, 'Do not use this program unmodified.'
    sys.exit(1)
    sys.exit(main())
