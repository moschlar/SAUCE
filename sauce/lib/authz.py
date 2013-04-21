# -*- coding: utf-8 -*-
'''
Created on 18.03.2012

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging

#TODO: Use environ instead of request if possible
from tg import request

from repoze.what.predicates import Predicate
from warnings import warn

log = logging.getLogger(__name__)


class has(Predicate):
    '''Generic request.user attribute checker class'''

    message = u'The user must be a %(attribute)s for this %(name)s'

    def __init__(self, attribute, obj, *args, **kwargs):
        self.attribute = attribute
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(has, self).__init__(*args, **kwargs)

    def evaluate(self, environ, credentials):
        attr = getattr(self.obj, self.attribute, None)
        if request.user == attr or request.user in attr:
            return
        self.unmet()


class has_student(Predicate):
    '''Check user access for given object type and id'''

    message = u'The user must be a student for this %(name)s'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        try:
            self.student = self.obj.student
        except:
            self.student = None
        super(has_student, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if request.student and request.student == self.student:
            return
        self.unmet()


class has_user(Predicate):

    message = u'The user must be attributed for this %(name)s'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        try:
            self.user = self.obj.user
        except:
            self.user = None
        super(has_user, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if request.user and request.user == self.user:
            return
        self.unmet()


class in_team(Predicate):

    message = u'The user must be in a team for this %(name)s'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        try:
            self.teams = self.obj.teams
        except:
            self.teams = []
        super(in_team, self).__init__(*args, **kwargs)

    def evaluate(self, environ, credentials):
        if getattr(request.user, 'teams', False):
            if set(request.user.teams) & set(self.teams):
                return
        self.unmet()


class has_teacher(Predicate):

    message = u'The user must be the teacher for this %(name)s'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        try:
            self.teachers = self.obj.teachers
        except:
            self.teachers = set()
        try:
            self.teacher = self.obj.teacher
            self.teachers.add(self.obj.teacher)
        except:
            self.teacher = None
        super(has_teacher, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if request.teacher and request.teacher in self.teachers:
            return
        self.unmet()


class has_teachers(Predicate):

    message = u'The user must be a teacher for this %(name)s'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        self.id = id
        try:
            self.teachers = self.obj.teachers
        except:
            self.teachers = set()
        try:
            self.teacher = self.obj.teacher
            self.teachers.add(self.teacher)
        except:
            self.teacher = None
        super(has_teachers, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if request.teacher and request.teacher in self.teachers:
            return
        self.unmet()


class is_public(Predicate):
    '''Check if given object is public'''

    message = u'This %(name)s must be public'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(is_public, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if not getattr(self.obj, 'public', True):
            self.unmet()
        return


class is_teacher(Predicate):

    message = u'The user must be a teacher'

    def evaluate(self, environ, credentials):
        warn("The predicate is_teacher() is not working anymore")
        if request.teacher:
            return
        self.unmet()
