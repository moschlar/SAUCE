#!/usr/bin/env python
'''
This script can be used to compile user and lesson/group data
from various sources in various formats into one single files
with columns suitable for the use by add_users.py.

You have, of course, to modify this file to suit your needs.
'''
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

import csv
from pprint import pprint

import sys
print >>sys.stderr, 'Do not use this program unmodified.'
sys.exit(1)


d = csv.DictReader(open('DSEA Teilnehmer.csv'), ['id', 'matrnr', 'nachname', 'vorname', 'x1', 'x2', 'email', 'x3', 'x4', 'sem', 'stat'], delimiter=';')

users_ = list(d)
users = dict()

for row in users_:
	for k in row:
		row[k] = row[k].decode('utf-8')
	users[row['nachname'], row['vorname']] = row
	pprint(row)

groups = dict()

f = open('dsea-Gruppen.txt')

i = 0
for line in f:
	line = line.strip().decode('utf-8')
	if line:
		if line.startswith(u'GRUPPE'):
			i += 1
		else:
			nachname, vorname = line.split(', ', 1)
			groups[nachname, vorname] = i
pprint(groups)

print "Inconsistencies: "

userset = set(users.iterkeys())
groupset = set(groups.iterkeys())

print "Only in users file: %s" % sorted(userset - groupset)
print "Only in groups file: %s" % sorted(groupset - userset)

d = csv.DictWriter(open('dsea_compiled.csv', 'w'), ['user_name', 'last_name', 'first_name', 'email_address', 'lesson_id'], delimiter=';')
d.writeheader()

for n, v in userset & groupset:
	d.writerow(dict(
		user_name=users[n, v]['email'].split('@', 1)[0].encode('utf-8'),
		last_name=users[n, v]['nachname'].encode('utf-8'),
		first_name=users[n, v]['vorname'].encode('utf-8'),
		email_address=users[n, v]['email'].encode('utf-8'),
		lesson_id=groups[n, v]
	))
