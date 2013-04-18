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
from sqlalchemy.orm.exc import NoResultFound


def load_config(filename):
    conf = appconfig('config:' + os.path.abspath(filename))
    load_environment(conf.global_conf, conf.local_conf)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("conf_file", help="configuration to use")
    parser.add_argument("csv_file", help="csv file to parse")
    parser.add_argument("csv_fields", default='firstrow', nargs='?',
                        help="csv field names, comma separated - field names that match a database field get used")
    return parser.parse_args()


def main():
    args = parse_args()
    load_config(args.conf_file)

    #event = model.Event.by_url(args.event_url)

    if args.csv_fields == 'firstrow':
        fields = None
    else:
        fields = args.csv_fields

    with open(args.csv_file) as f:
        reader = csv.DictReader(f, fieldnames=fields, dialect=csv.excel_tab)
        dicts = list(reader)

    errors = []

    for d in dicts:
        print d
        try:
            s = model.User.query.filter_by(user_name=d['user_name']).one()
        except NoResultFound:
            s = model.User(user_name=d['user_name'])
            model.DBSession.add(s)
        s._last_name = d['last_name'].decode('utf-8')
        s._first_name = d['first_name'].decode('utf-8')
        s.email_address = d['email_address']

        try:
            #model.DBSession.flush()
            transaction.commit()
        except SQLAlchemyError as e:
            #model.DBSession.rollback()
            transaction.abort()
            #print e.message
            errors.append((e, s))
            #raise e

#    try:
#        transaction.commit()
#    except SQLAlchemyError as e:
#        transaction.abort()
#        raise e

    print errors

if __name__ == '__main__':
    print >>sys.stderr, 'Do not use this program unmodified.'
    sys.exit(1)
    sys.exit(main())
