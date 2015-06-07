'''
@since: 16.04.2014

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

import transaction

from sauce.tests import load_app, setup_app, teardown_db
from sauce import model


__all__ = ['test_model_urls']

app = None
''':type app: webtest.TestApp'''


def setUpModule():
    global app
    app = load_app()
    setup_app()

    # Prepare nullable=True test data
    u = model.User(id=0, user_name='empty', email_address='empty', display_name=None, created=None)
    e = model.Course(id=0, name='Empty', _url='empty', description=None, enabled=True)
    s = model.Sheet(id=0, name='Empty', sheet_id='0', event=e, description=None)
    a = model.Assignment(id=0, name='Empty', assignment_id='0', sheet=s, description=None, timeout=None)
    ss = model.Submission(id=0, user=u, assignment=a, filename=None, source=None, language=None)
    j = model.Judgement(id=0, submission=ss, tutor=u)
    model.DBSession.add_all((u, e, a, s, ss, j))
    transaction.commit()


def tearDownModule():
    model.DBSession.remove()
    teardown_db()


# Get all model classes that have an url attribute
entities = [x for x in model.__dict__.itervalues()
    if isinstance(x, type) and issubclass(x, model.DeclarativeBase) and hasattr(x, 'url')
        and not x.__name__ in ('Course', 'Contest')]

extra_environ = {'REMOTE_USER': 'manager'}


def _test_model_url(url):
    if url:
        return app.get(url, extra_environ=extra_environ)
    else:
        return None


def test_model_urls():
    for entity in entities:
        for instance in entity.query:
            instance = model.DBSession.merge(instance)  # Why???
            yield _test_model_url, instance.url


if __name__ == '__main__':
    print entities
