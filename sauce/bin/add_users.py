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


def main():
    args = parse_args()
    load_config(args.conf_file)

    #event = model.Event.by_url(args.event_url)

    dicts = []

    with open(args.csv_file) as f:
        for line in f:
            d = {}
            line = line.decode('utf-8').strip()
            _, last, rest = line.split('\t', 2)
            first, user = rest.rsplit('\t', 1)
            d['user_name'] = user
            d['email_address'] = user + '@students.uni-mainz.de'
            d['display_name'] = first + ' ' + last
            dicts.append(d)

    errors = []

    for d in dicts:
        print d
        s = model.User.query.filter_by(user_name=d['user_name']).first()
        if not s:
            s = model.User(user_name=d['user_name'],
                display_name=d['display_name'],
                email_address=d['email_address'])
            print s

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

    print errors

if __name__ == '__main__':
#     print >>sys.stderr, 'Do not use this program unmodified.'
#     sys.exit(1)
    sys.exit(main())
