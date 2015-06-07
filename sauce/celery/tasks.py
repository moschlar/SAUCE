# -*- coding: utf-8 -*-
from __future__ import absolute_import
from time import sleep
from sauce.celery import app


@app.task
def run(arg):
    print arg
    print 'Sleeping for 10'
    sleep(10)
    result = dict(result=arg['source_code'][:10])
    return result
