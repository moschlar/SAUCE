#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Created on 08.07.2012

@author: moschlar
'''

#######################################################################
# Fill in your comparison function here
from difflib import SequenceMatcher
comparison = lambda s1, s2: SequenceMatcher(a=s1, b=s2).ratio()
#######################################################################

FILENAME_IN = 'submissions.pkl'
FILENAME_OUT = 'submissions_similarity.pkl'

import os, sys, time, argparse
from multiprocessing import Pool
try:
    import cPickle as pickle
except ImportError:
    import pickle


def worker(s):
    s1, s2 = s
    return (s1, s2, comparison(s1['source'] or u'', s2['source'] or u''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate similarity matrix from pickled data')
    parser.add_argument('-l', '--list', action='store_true', dest='list',
        help='list all assignments from the INPUT_FILE')
    parser.add_argument('-i', '--in', metavar='INPUT_FILE',
        type=argparse.FileType('rb'), default=FILENAME_IN, dest='infile')
    parser.add_argument('-o', '--out', metavar='OUTPUT_FILE',
        type=argparse.FileType('wb'), default=FILENAME_OUT, dest='outfile')
    parser.add_argument('-a', '--all', action='store_true', dest='all',
        help='generate similarity data for all assignments from the INPUT_FILE '
        '(This can take some time)')
    parser.add_argument('assignments', nargs='*', type=int,
        help='assignment ids')
    args = parser.parse_args()

    with args.infile as pf:
        assignments = pickle.load(pf)

    if args.list:
        print '%3s %-60s %3s' % ('id', 'name', 'submissions')
        for a in assignments:
            print '%3d %-60s %3d' % (a['id'], '"%s"' % a['name'], len(a['submissions']))
        sys.exit(0)

    if not args.all and not args.assignments:
        print 'You need to specify either --all or a list of assignment ids'
        parser.print_help()
        sys.exit(1)

    if args.assignments:
        assignments = [a for a in assignments if a['id'] in args.assignments]

    for assignment in assignments:
        # assignment:
        # ['assignment_id', 'sheet_id', 'submissions', 'name', 'id']
        print len(assignment['submissions'])
        start = time.time()
        matrix = dict()
        p = Pool()
        for s1 in assignment['submissions']:
            matrix[s1['id']] = dict()
            for s2 in assignment['submissions']:
                for (a, b, value) in p.map(worker, ((s1, s2) for s2 in assignment['submissions'])):
                    matrix[a['id']][b['id']] = value
        p.close()
        p.join()
        print matrix
        del assignment['submissions']
        assignment['similarity'] = matrix
        assignment['time'] = time.time() - start

    print assignments

    with args.outfile as pf:
        pickle.dump(assignments, pf)

