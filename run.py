#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Start the Paster server

Given command line arguments will be passed through
'''

import sys
from paste.script.serve import ServeCommand
ServeCommand("serve").run(sys.argv[1:])
