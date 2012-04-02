#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Start the Paster server

Given command line arguments will be passed through
'''

import sys
from paste.script.serve import ServeCommand

if __name__ == '__main__':
    if len(sys.argv) == 1:
        args = ['--reload', 'development.ini']
    else:
        args = sys.argv[1:]
    ServeCommand("serve").run(args)
