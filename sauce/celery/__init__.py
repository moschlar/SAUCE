# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Celery, Task

app = Celery('sauce',
             broker='amqp://',
             backend='rpc://',
             include=['sauce.celery.tasks'])

app.conf.update(
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_TRACK_STARTED=True,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    # CELERY_RESULT_PERSISTENT=True,
    CELERY_SEND_EVENTS=True,
)

if __name__ == '__main__':
    app.start()