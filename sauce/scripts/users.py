#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Add new users via console.

@author: moschlar
"""
import os
import sys
from getpass import getpass
from argparse import ArgumentParser
import traceback

from sqlalchemy.exc import IntegrityError

from paste.deploy import appconfig
from sauce.config.environment import load_environment
from sauce import model
from sauce.model import DBSession as Session

import transaction

def load_config(filename):
    conf = appconfig('config:' + os.path.abspath(filename))
    load_environment(conf.global_conf, conf.local_conf)

def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("conf_file", help="configuration to use")
    return parser.parse_args()

def main():
    args = parse_args()
    load_config(args.conf_file)
    
    #print model.DBSession.query(model.User.user_name).all()
    
    events = Session.query(model.Event).all()
    
    print [(i, e.name) for i,e in enumerate(events)]
    
    event_id = raw_input('event_id: ')
    event = events[int(event_id)]
    
    while True:
        teamname = raw_input("Team-Name: ")
        if not isinstance(teamname, unicode):
            teamname = teamname.decode('utf-8')
        password = getpass("Password: ")
        if not isinstance(password, unicode):
            password = password.decode('utf-8')
        team = model.Team(name=teamname)
        team.events.append(event)
        Session.add(team)
        
        student = model.Student(user_name=teamname, display_name=teamname, 
                                email_address=teamname+'@students.uni-mainz.de',
                                password=password, teams=[team])
        Session.add(student)
        
        try:
            transaction.commit()
        except IntegrityError:
            print traceback.format_exc()
            transaction.abort()
        
        next = raw_input("Next Team? [y]")
        if next != 'y':
            break

if __name__ == '__main__':
    sys.exit(main())
