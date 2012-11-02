#!/usr/bin/env python
'''
This script can be used to compile user and lesson/group data
from various sources in various formats into one single files
with columns suitable for the use by add_users.py.

You have, of course, to modify this file to suit your needs.
'''

import csv
from pprint import pprint

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

