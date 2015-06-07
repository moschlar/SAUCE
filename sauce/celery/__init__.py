# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Celery, Task

app = Celery('sauce',
             broker='amqp://',
             backend='amqp://',
             include=['sauce.celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TRACK_STARTED=True,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    # CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()