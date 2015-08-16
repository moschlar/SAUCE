# -*- coding: utf-8 -*-
from __future__ import absolute_import
import jsonpickle
from time import sleep, time
from celery.utils.log import get_task_logger

from sauce.celery import app
from sauce.lib.serialize import Undictifier


logger = get_task_logger(__name__)


# TODO: http://docs.celeryproject.org/en/latest/userguide/tasks.html#custom-states
# TODO: Maybe put result harvesting job on main node

@app.task(bind=True, expires=60*60)  # Expire after one hour
def run_tests(self, submission):
    submission = jsonpickle.loads(submission)
    undictifier = Undictifier(submission)
    submission = undictifier()

    (compilation, testruns, result) = submission.run_tests()

    testruns = [t._replace(test=t.test.id) for t in testruns]

    return jsonpickle.dumps((compilation, testruns, result))
