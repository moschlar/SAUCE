# -*- coding: utf-8 -*-
'''Submission model module

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
from datetime import datetime
from difflib import unified_diff
from time import time

from tg.caching import cached_property

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import backref, deferred, relationship
from sqlalchemy.sql import desc
from sqlalchemy.types import Boolean, DateTime, Float, Integer, PickleType, Unicode

from sauce.lib.helpers import link
from sauce.lib.runner import Runner
from sauce.model import DBSession, DeclarativeBase
from sauce.model.event import Lesson
from sauce.model.test import Testrun
from sauce.model.user import Team, User


__all__ = ('Submission', 'Judgement')


log = logging.getLogger(__name__)


class Submission(DeclarativeBase):
    '''
    :type assignment: sauce.model.Assignment
    :type scaffold_head: str | None
    :type scaffold_head_lines: list[str] | None
    :type scaffold_head_lines_len: int
    :type scaffold_foot: str | None
    :type scaffold_foot_lines: list[str] | None
    :type scaffold_foot_lines_len: int
    '''
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, nullable=False)

    created = Column(DateTime, nullable=False, default=datetime.now,
        doc='Creation date of submission')
    modified = Column(DateTime, nullable=False, default=datetime.now,
        doc='Last modified date of submission')

    filename = Column(Unicode(255), nullable=True,
        doc='The submitted filename, if any')
    source = deferred(Column(Unicode(10 * 1024 * 1024), nullable=True), group='data',
        doc='The submitted source code')

    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False, index=True)
    assignment = relationship("Assignment",
        backref=backref('submissions',
            order_by=id,
            cascade='all, delete-orphan',
        )
    )

    language_id = Column(Integer, ForeignKey('languages.id'), nullable=True)
    language = relationship('Language')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    user = relationship('User',
        backref=backref('submissions',
            order_by=id,
            cascade='all, delete-orphan')
        )

    public = Column(Boolean, nullable=False, default=False,
        doc='Whether this submission is publicly accessible by anyone')

    comment = Column(Unicode(1024 * 1024), nullable=True,
        doc='An additional comment on the whole submission')

#    complete = Column(Boolean, default=False)
#    '''Whether submission is finally submitted or not'''

    __mapper_args__ = {'order_by': [desc(created), desc(modified)]}

    def __repr__(self):
        return (u'<Submission: id=%r, assignment_id=%r, user_id=%r>'
            % (self.id, self.assignment_id, self.user_id)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Submission %s' % (self.id or '')

    @property
    def full_source(self):
        # This method adds at most two \n to the return value
        src = []
        if self.assignment.submission_scaffold_head:
            src.append(self.assignment.submission_scaffold_head)
        if self.source:
            src.append(self.source)
        if self.assignment.submission_scaffold_foot:
            src.append(self.assignment.submission_scaffold_foot)
        return '\n'.join(src) if src else ''

    @cached_property
    def scaffold_show(self):
        return self.assignment.submission_scaffold_show

    @cached_property
    def scaffold_head(self):
        ''':rtype: str | None'''
        return self.assignment.submission_scaffold_head or None

    @cached_property
    def scaffold_head_lines(self):
        ''':rtype: list[str] | None'''
        return self.assignment.submission_scaffold_head_lines

    @cached_property
    def scaffold_head_lines_len(self):
        ''':rtype: int'''
        return self.assignment.submission_scaffold_head_lines_len

    @cached_property
    def scaffold_foot(self):
        ''':rtype: str | None'''
        return self.assignment.submission_scaffold_foot or None

    @cached_property
    def scaffold_foot_lines(self):
        ''':rtype: list[str] | None'''
        return self.assignment.submission_scaffold_foot_lines

    @cached_property
    def scaffold_foot_lines_len(self):
        ''':rtype: int'''
        return self.assignment.submission_scaffold_foot_lines_len

    @cached_property
    def source_lines_len(self):
        ''':rtype: int'''
        return len(self.source.splitlines()) if self.source else 0

    @cached_property
    def scaffold_line_numbers(self):
        ''':rtype: (int, int, int, int)'''
        # TODO: The numbers work but look pretty unintuitive
        start_head = 0
        end_head = start_head + self.scaffold_head_lines_len
        len_src = self.source_lines_len
        start_foot = end_head + len_src
        end_foot = start_foot + self.scaffold_foot_lines_len
        return start_head, end_head, start_foot, end_foot

    def run_tests(self):

        compilation = None
        testruns = []
        result = False

        # Consistency checks
        if self.language and self.full_source and self.assignment:
            with Runner(self) as r:
                log.debug('Starting Runner for submission %r', self)
                # First compile, if needed
                compilation = r.compile()
                if compilation:
                    log.debug('Compilation runtime: %f', compilation.runtime)
                    log.debug('Compilation result: %s', compilation.result)

                if not compilation or compilation.result:
                    # Delete old testruns
                    self.testruns = []
                    #DBSession.flush()

                    # Then run all the tests
                    testruns = []
                    start = time()
                    for t in r.test():
                        testruns.append(t)
                        self.testruns.append(
                            Testrun(
                                submission=self, test=t.test,
                                result=t.result, partial=t.partial,
                                runtime=t.runtime,
                                output_data=t.output_data,
                                error_data=t.error_data,
                            )
                        )
                    end = time()
                    test_time = end - start
                    log.debug('Test runs total runtime: %f', test_time)
                    log.debug('Test runs results: %r', list(str(t.result) for t in testruns))

                    try:
                        DBSession.flush()
                    except:
                        log.exception('Could not save testrun results')
                        raise

                    result = self.result
                    log.debug('Test runs result: %s ', result)
                else:
                    log.debug('Test runs not run')
        return (compilation, testruns, result)

    @property
    def name(self):
        return unicode(self)

    @property
    def url(self):
        return '/submissions/%s' % self.id

    @property
    def link(self):
        return link('Submission %d' % self.id, self.url)

    @property
    def parent(self):
        '''Parent entity for generic hierarchy traversal'''
        return self.assignment

    @property
    def visible_testruns(self):
        return list(testrun for testrun in self.testruns if testrun.test.visible)

# Not usable since student may have no team
#    @property
#    def team(self):
#        try:
#            return self.student.team_by_event(self.assignment.event)
#        except:
#            return None

    @property
    def result(self):
        if self.testruns:
            for t in self.testruns:
                if not t.result:
                    return False
            return True
        return None

    @property
    def runtime(self):
        return sum(t.runtime for t in self.testruns)

    @property
    def testrun_date(self):
        try:
            return sorted(self.testruns, key=lambda t: t.date).pop().date
        except IndexError:
            return None

    @property
    def teams(self):
        '''Returns a list of teams that are eligible for this submission'''
        teams = set()
        for lesson in self.assignment.sheet.event.lessons:
            teams |= set(lesson.teams)
        teams &= set(self.user.teams)
        return teams

    @property
    def team(self):
        if self.teams:
            if len(self.teams) == 1:
                return self.teams.pop()
            else:
                log.warn('Submission %r has ambiguous team reference', self)
                return None
        else:
            return None

    @property
    def lessons(self):
        lessons = set(self.user.lessons) & set(self.assignment.sheet.event.lessons)
        return lessons

    def newer_submissions(self):
        class Newer(object):
            '''You may use me like a list'''
            user = []
            team = []

            def __iter__(self):
                for i in self.user + self.team:
                    yield i

            def __len__(self):
                return len(self.user) + len(self.team)

            def __getitem__(self, i):
                return sorted(self.user + self.team, key=lambda s: s.modified, reverse=True)[0]

        newer = Newer()

        newer.user = (Submission.by_assignment_and_user(self.assignment, self.user)
            .filter(Submission.modified > self.modified).order_by(desc(Submission.modified)).all())
        newer.team = []
        if hasattr(self.user, 'teams'):
            for team in self.teams:
                for member in team.members:
                    if member != self.user:
                        newer.team.extend(Submission.by_assignment_and_user(self.assignment, member)
                            .filter(Submission.modified > self.modified).order_by(desc(Submission.modified)).all())
        return newer

    @classmethod
    def by_assignment_and_user(cls, assignment, user):
        return cls.query.filter_by(assignment_id=assignment.id).filter_by(user_id=user.id)

    @classmethod
    def by_teacher(cls, teacher):
        return (cls.query.join(Submission.user).join(User.teams).join(Team.lesson)
            .filter(Lesson.tutor == teacher).order_by(desc(Submission.created)).order_by(desc(Submission.modified)))


class Judgement(DeclarativeBase):
    __tablename__ = 'judgements'

    id = Column(Integer, primary_key=True, nullable=False)

    date = Column(DateTime, nullable=False, default=datetime.now,
        doc='Date of judgement')

    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False, index=True)
    submission = relationship('Submission',
        backref=backref('judgement',
            uselist=False,
            cascade='all, delete-orphan',
        )
    )

    # TODO: Rename to user
    tutor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutor = relationship('User',
        backref=backref('judgements',
            cascade='all, delete-orphan',
        )
    )

    #testrun_id = Column(Integer, ForeignKey('testruns.id'))
    #testrun = relationship('Testrun',
    #    backref=backref('judgement', uselist=False)
    #    )

    corrected_source = deferred(Column(Unicode(10 * 1024 * 1024), nullable=True), group='data',
        doc='Tutor-corrected source code')

    comment = Column(Unicode(1024 * 1024), nullable=True,
        doc='An additional comment on the whole submission')

    annotations = Column(PickleType, nullable=True,
        doc='Per-line annotations should be a dict using line numbers as keys')

    grade = Column(Float, nullable=True)

    public = Column(Boolean, nullable=False, default=True,
        doc='Whether this judgement is accessible to those who can access the submission')

    def __repr__(self):
        return (u'<Judgement: id=%r, submission_id=%r, tutor_id=%r>'
            % (self.id, self.submission_id, self.tutor_id)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Judgement %d for Submission %d' % (self.id or '', self.submission_id or '')

    @property
    def parent(self):
        return self.submission

    @property
    def diff(self):
        return ''.join(unified_diff(
            self.submission.source.splitlines(True) if self.submission.source else '',
            self.corrected_source.splitlines(True) if self.corrected_source else '',
            'your source', 'corrected source')
        )
