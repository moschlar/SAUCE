# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Celery, Task

app = Celery('sauce',
             broker='amqp://',
             backend='rpc://',
             include=['sauce.celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_TRACK_STARTED=True,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_RESULT_PERSISTENT=True,
    CELERY_SEND_EVENTS=True,
)

state = None

def my_monitor(app):
    global state
    state = app.events.State()

    def print_event(event):
        if event['type'] != 'worker-heartbeat':
            print event['type'], event
        state.event(event)

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                '*': print_event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    app.start()