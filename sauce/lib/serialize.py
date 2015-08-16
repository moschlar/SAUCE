# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
from functools import partial

from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy_utils import get_mapper

from jsonpickle.util import importable_name
from jsonpickle.unpickler import loadclass

from sauce.model import *


class Dictifier(object):

    def __init__(self, exclude=None):
        self.data = defaultdict(dict)
        self.exclude = exclude or ()

    def _dictify_list(self, list):
        data = []
        for item in list:
            data.append(self._dictify_object(item))
        return data

    def _dictify_object(self, obj):
        mapper = get_mapper(obj)
        entity = importable_name(mapper.entity)
        pk = mapper.primary_key_from_instance(obj).pop()

        if pk not in self.data[entity]:
            self.data[entity][pk] = data = {}
            for prop in mapper.iterate_properties:
                if (mapper.entity, prop.key) not in self.exclude:
                    attr = getattr(obj, prop.key)
                    if isinstance(prop, ColumnProperty):
                        data[prop.key] = getattr(obj, prop.key)
                    if isinstance(prop, RelationshipProperty):
                        if prop.mapper.entity not in self.exclude:
                            if prop.uselist:
                                data[prop.key] = self._dictify_list(attr) if attr else []
                            else:
                                data[prop.key] = self._dictify_object(attr) if attr else None
        return entity, pk

    def __call__(self, obj):
        self.data['_start'] = self._dictify_object(obj)
        return self.data


class Undictifier(object):

    def __init__(self, data):
        self.objs = defaultdict(dict)
        self.data = data

    def _undictify_list(self, list):
        data = []
        for item in list:
            data.append(self._undictify_object(*item))
        return data

    def _undictify_object(self, entity, pk):
        cls = loadclass(entity)
        mapper = get_mapper(cls)

        pk = unicode(pk)

        if pk not in self.objs[entity]:
            data = self.data[entity][pk]

            self.objs[entity][pk] = obj = cls()

            for prop in mapper.iterate_properties:
                attr = data.get(prop.key, None)
                if attr:
                    if isinstance(prop, ColumnProperty):
                        setattr(obj, prop.key, attr)
                    if isinstance(prop, RelationshipProperty):
                        if prop.uselist:
                            data[prop.key] = self._undictify_list(attr)
                        else:
                            setattr(obj, prop.key, self._undictify_object(*attr))

        return self.objs[entity][pk]

    def __call__(self, start=None):
        entity, pk = start or self.data['_start']
        obj = self._undictify_object(entity, pk)
        return obj


submission_excludes = (
    LTI, User, Group, Permission, Team, Lesson, Judgement, Testrun,
    (Assignment, 'allowed_languages'), (Assignment, 'submissions'),
    (Sheet, 'assignments'), (Event, 'sheets'),
)

SubmissionDictifier = partial(Dictifier, exclude=submission_excludes)

# testrun_excludes = (
#     LTI, User, Group, Permission, Team, Lesson, Judgement,
#     Language, Compiler, Interpreter,
#     Assignment, Sheet, Event,
# )
#
# TestrunDictifier = partial(Dictifier, exclude=testrun_excludes)


def main(submission_id):
    from sauce.model import Submission
    submission = Submission.query.get(submission_id)
    dictifier = Dictifier(exclude=(
            User, Group, Permission, Team, Lesson, Testrun, Judgement, LTI,
            (Assignment, 'allowed_languages'), (Assignment, 'submissions'),
            (Sheet, 'assignments'), (Event, 'sheets'),
        )
    )
    data = dictifier(submission)
    from pprint import pprint
    pprint(dict(data))
    undictifier = Undictifier(data)
    obj = undictifier()
    pprint(obj)
    print obj.full_source, obj.assignment, obj.assignment.tests[0]
    raise
    s = dictify_submission(submission)
    s = dictify_submission(submission)
    print s
    import anyjson
    # print anyjson.dumps(s)
    import jsonpickle
    print jsonpickle.dumps(s)
    print jsonpickle.loads(jsonpickle.dumps(s))