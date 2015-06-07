# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""
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

from nose.tools import eq_
from sauce.model import DBSession
from sauce.tests import load_app, setup_db, teardown_db

__all__ = ['ModelTest']


# Create an empty database before we start our tests for this module
def setup():
    """Setup test fixture for all model tests."""
    load_app()
    setup_db()


# Tear down that database
def teardown():
    """Tear down test fixture for all model tests."""
    teardown_db()


class ModelTest(object):
    """Base unit test case for the models."""

    klass = None
    attrs = {}

    def setUp(self):
        """Setup test fixture for each model test method."""
        try:
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass(**new_attrs)
            DBSession.add(self.obj)
            DBSession.flush()
            return self.obj
        except:
            DBSession.rollback()
            raise

    def tearDown(self):
        """Tear down test fixture for each model test method."""
        DBSession.rollback()

    def do_get_dependencies(self):
        """Get model test dependencies.

        Use this method to pull in other objects that need to be created
        for this object to be build properly.

        """
        return {}

    def test_create_obj(self):
        """Model objects can be created"""
        pass

    def test_query_obj(self):
        """Model objects can be queried"""
        obj = DBSession.query(self.klass).one()
        for key, value in self.attrs.items():
            eq_(getattr(obj, key), value)
