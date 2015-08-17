# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery import Celery, Task


# def register_jsonpickle():
#     ''':py:func:`kombu.serialization.register_json`'''
#     from kombu.serialization import registry
#     from kombu.utils.encoding import bytes_t
#     from jsonpickle import loads as json_loads, dumps as json_dumps
#
#     def _loads(obj):
#         if isinstance(obj, bytes_t):
#             obj = obj.decode()
#         return json_loads(obj)
#
#     registry.register('json', json_dumps, _loads,
#                       content_type='application/json',
#                       content_encoding='utf-8')
#
# register_jsonpickle()


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

# TODO: __main__.py

if __name__ == '__main__':
    app.start()
