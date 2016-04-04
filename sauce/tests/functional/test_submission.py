# -*- coding: utf-8 -*-
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

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

import status

from sauce.tests import load_app, setup_app, teardown_db
from sauce import model


__all__ = ['TestSubmissionController']

app = None
''':type app: webtest.TestApp'''


def setUpModule():
    global app
    app = load_app()
    setup_app()


def tearDownModule():
    model.DBSession.remove()
    teardown_db()


#http://generator.lorem-ipsum.info/
#koi8-r
cyrillic_stuff = '\xee\xdc \xc8\xc1\xd6 \xcb\xcf\xce\xd3\xdc\xcb\xd7\xc0\xc1\xd4 \xc4\xd9\xc6\xd1\xce\xc9\xdc\xc2\xc1\xd6, \xdc\xc0 \xc5\xc0\xd6 \xcb\xd7\xc0\xc1\xd9\xcb\xd7\xd5\xdc \xd6\xd1\xcd\xc9\xcc\xd1\xcb\xd7\xc0\xd9 \xc1\xcb\xcb\xcf\xcd\xcd\xcf\xc4\xc1\xd2\xd9? \xe5\xc4 \xc9\xd0\xda\xd5\xcd \xc0\xd2\xc2\xc1\xce\xca\xd4\xc1\xd6 \xc9\xce\xda\xd4\xd2\xd5\xcb\xd4\xc5\xcf\xd2 \xcb\xc0\xcd, \xd0\xd2\xcf \xda\xcf\xcc\xdc\xd4 \xcd\xc1\xcc\xd8\xcf\xd2\xd5\xcd \xcb\xcf\xce\xd7\xd9\xce\xa3\xd2\xd9 \xdc\xc1! \xe9\xce\xcb\xc5\xc4\xd9\xd2\xc9\xce\xd4 \xcb\xcf\xce\xde\xdc\xcb\xd4\xdc\xd4\xc0\xd9\xd2 \xcb\xd5 \xc5\xc0\xd6, \xd0\xdc\xd2 \xcd\xc1\xc9\xcf\xd2\xc0\xcd \xcd\xc1\xce\xc4\xc1\xcd\xc0\xde \xd4\xd9. \xf6\xd1\xd4 \xd4\xd9 \xca\xd5\xd6\xd4\xcf \xda\xc1\xcc\xd8\xc0\xd4\xc1\xd4\xd5\xd6, \xc9\xd0\xda\xd5\xcd \xc9\xc7\xce\xcf\xd4\xc1 \xcd\xdc\xcc\xd8 \xce\xdc. \xe4\xd5\xcf \xcb\xd7\xc0\xc9\xd6 \xcd\xcf\xd7\xdc\xd4 \xcd\xc0\xce\xd9\xd2\xdc \xce\xdc, \xdc\xc0 \xdc\xd2\xd2\xdc\xcd \xce\xd9\xcd\xcf\xd2\xdc \xc8\xdc\xce\xc4\xd2\xdc\xd2\xc5\xd4 \xd7\xd1\xdb, \xcd\xc1\xc7\xce\xc1 \xd7\xd9\xcc\xd8\xa3\xd4 \xcb\xcf\xd2\xd2\xc0\xcd\xd0\xc9\xd4 \xc8\xc1\xd6 \xc1\xce.'
#iso-8859-7
greek_stuff = '\xd6\xe9\xe4\xe5\xf1\xe5\xf1 \xf3\xf9\xed\xf3\xe5\xea\xf5\xe1\xe8 \xf3\xe9\xe8 \xe5\xe1, \xf9\xec\xed\xe9\xf5\xec \xf6\xe1\xf3\xe9\xeb\xe9\xf2 \xe5\xee\xf0\xeb\xe9\xf3\xe1\xf1\xe9 \xe5\xf5 \xec\xe5\xeb, \xf6\xe5\xeb \xe1\xeb\xe9\xea\xf5\xe9\xe4 \xf0\xe1\xf1\xf4\xe9\xe5\xed\xe4\xf9 \xed\xe5? \xcc\xe5\xe1 \xe1\xf4 \xec\xef\xe4\xf5\xf2 \xeb\xf5\xf3\xe9\xeb\xe9\xf5\xf2. \xc1\xeb\xe9\xe5\xed\xf5\xec \xeb\xe5\xe3\xe5\xed\xe4\xf9\xf2 \xf7\xe5\xed\xe4\xf1\xe5\xf1\xe9\xf4 \xf3\xf5 \xf6\xe5\xeb. \xd0\xf1\xf9 \xf5\xe8 \xe5\xf3\xe5\xed\xf4 \xf0\xe5\xf1\xf3\xe5\xf3\xf5\xf4\xe9 \xe7\xf9\xed\xe5\xf3\xe8\xe1\xe8\xe9\xf2, \xf6\xe9\xec \xe1\xe4\xf7\xf5\xf2 \xf6\xe5\xf5\xe3\xe9\xe1\xe8 \xe1\xed! \xc8\xe5 \xe9\xf5\xf3\xe8\xef \xf6\xe1\xf3\xe5\xf1 \xe5\xf5\xec, \xed\xe5 \xec\xe5\xe1 \xf6\xe9\xe4\xe9\xf4 \xec\xe5\xed\xe1\xed\xe4\xf1\xe9 \xe4\xe5\xf6\xe9\xed\xe9\xe8\xe9\xef\xed\xe5\xec. \xc9\xe4 \xe4\xf9\xf3\xe5\xed\xe4\xe9 \xe5\xee\xf0\xe5\xe8\xe5\xed\xe4\xe9\xf2 \xe5\xf5\xec.'
#gbk
chinese_stuff = '\xd9V\xbf\xbc\xbco\xbc\xbc\xb6\xa8\xd5\xfe\xc8\xaf\xd1\xdd\xd6\xce\xd3\xe8\xcc\xef\x90\x99\xd7\xd4\xb1h\xbe\xd6\xa1\xa3\xc9\xcf\xeby\xb1\xd8\xd3\xc9\xd4\xe7\xd2\xe2\x98S\x92\xf7\xd3\xfd\xd2\xbd\xc3\xd7\xd6\xed\xa1\xa3\xe9L\xb5\xd6\xd6\xce\xdfB\xbb\xc4\xbc\xa4\xc5\xae\xb6\xa8\x9a\xa2\xc2\x84\xb6\xcf\xd9R\xd5\xd1\xcb\xbc\xca\xb8\xbdK\xddd\xa1\xa3\x9cg\xd3E\xb4\xf2\xdfx\x84\xa1\x9cg\xbf\xd5\xca\xa7\xd1a\xca\xd6\xb4\xe5\xc3\xfb\xdb\xe0\xd7\xd3\xb9\xa6\x83P\xc8\xcb\xd4\xc2\xc0\xfd\xd5i\xa1\xa3\xdfh\xcb\xcd\x9fo\xbdU\xd1\xd2\xbe\xa9\xb2\xbb\xd0\xa3\x81K\xcc\xbd\xb4\xa5\xb1\xbe\x8f\xea\xbf\xb9\xa1\xa3\xb2\xa9\xd3\xf9\xd0\xc2\x92i\xd7\xee\x95\xf8\xdf`\xbd\xfb\xb1\xed\xdfB\xbc\xd3\xb9\xa9\xd7\xd4\xa1\xa3\x9f\xeb\xd0\xdb\x92B\xc4\xba\xc0\xed\x8aZ\xd0\xc2\x95\xf8\xd4\x92\xc2\xa9\xbe\xb3\xc6\xf3\xb1\xb3\xa1\xa3\xb3\xf6\xc9\xcf\xd6\xf7\xc4\xba\xd6\xa2\xb8\xe6\xd2\x8a\x81K\x8e\xda\xbc\xd2\xc8\xcb\xd2\x95\xb3\xf6\xc9\xcc\xca\xcb\xb2\xbb\xbd\xb9\xb5\xb9\xca\xf4\xd3\xe8\xa1\xa3\xe9v\xd3\xfd\xd2\xb9\xd7\xf7\x83\xb9\xe9v\xb4\xee\xd2\xaa\xcd\xac\xbe\xb0\xcd\xc6\xbcs\xd2\x99\xd0\xc2\xba\xcd\xc9\xe7\xa1\xa3'
#euc-jp
japanese_stuff = '\xcc\xeb\xa5\xeb\xa4\xeb\xbd\xbb\xcc\xcc\xa4\xeb\xa4\xb0\xa4\xe0\xa4\xab\xbc\xcc\xba\xd0\xcd\xb6\xa4\xaa\xa5\xaf\xbd\xa9\xb9\xe7\xa4\xbe\xa4\xea\xa4\xc3\xa4\xd1\xbb\xd8\xb7\xee\xa4\xbf\xc9\xa9\xb5\xe5\xbb\xd1\xc2\xbc\xa4\xd2\xa4\xbd\xa4\xe2\xa4\xd5\xc6\xe2\xb2\xdd\xb6\xbd\xa4\xb6\xa4\xad\xbf\xde5\xc5\xcf\xa5\xef\xa5\xb9\xa5\xce\xa5\xc6\xc3\xe6\xbc\xd6\xb1\xdf\xb7\xb9\xa4\xe1\xa4\xbe\xa1\xa3\xce\xc3\xa5\xde\xa5\xdf\xa5\xea\xa5\xc1\xbf\xde\xcb\xcc\xa5\xbb\xa5\xa2\xa5\xb9\xc2\xae\xca\xe5\xa5\xb1\xa5\xbb\xa5\xea\xa5\xd2\xc0\xca\xc2\xe7\xa5\xb1\xa5\xef\xa5\xc8\xb4\xc643\xb6\xad\xa1\xbc\xb1\xdb\xbc\xa1\xb3\xcb\xb3\xda\xa5\xc8\xa5\xa4\xa5\xaf\xbb\xf6\xc9\xd4\xa4\xcb\xa4\xe2\xb0\xec\xc2\xe7\xa5\xb7\xc6\xc0\xb6\xd8\xa5\xeb\xa4\xb6\xa4\xb1\xa4\xc9\xb6\xc3\xc2\xd8\xa4\xc8\xa4\xe7\xa5\xa4\xa4\xa2\xc1\xed\xb6\xb5\xa4\xa2\xa4\xe0\xa4\xc8\xa4\xd2\xb1\xd2\xb3\xa8\xa4\xd0\xa4\xef\xa4\xb1\xa4\xd8\xc8\xd6\xca\xc9\xcf\xb3\xc4\xba\xb8\xe6\xa4\xd5\xa4\xc9\xa1\xa3\xbc\xd6\xa5\xb7\xa5\xab\xa5\xaf\xa5\xb3\xb2\xf0\xc1\xb0\xa5\xcb\xa5\xf2\xa5\xe2\xcc\xcc43\xb7\xfa\xa5\xd2\xa5\xe1\xa5\xca\xc6\xbb\xbb\xb0\xa5\xd8\xa5\xe9\xb2\xae\xbb\xdf\xcc\xe4\xc8\xd7\xa4\xd5\xeb\xbe\xbf\xbf\xa5\xc6\xa5\xbb\xa5\xad\xc1\xb0\xc8\xbd\xa5\xc8\xcb\xa1\xc0\xda\xa4\xdf\xbc\xbc\xbc\xc2\xa4\xbd\xa4\xc1\xa5\xc3\xc5\xcf\xb8\xa2\xa5\xef\xa5\xb1\xa5\xe9\xa5\xd8\xbc\xf8\xb2\xb9\xa5\xe0\xa5\xa2\xa5\xab\xa5\xf1\xc2\xc0\xc3\xce\xa5\xaf\xa4\xd5\xa4\xcb\xca\xb8\xc2\xe5\xa4\xaf\xa4\xba\xc2\xda94\xb2\xad\xa4\xe2\xa4\xb6\xa1\xa3'

class TestSubmissionController(TestCase):

    environ = {'REMOTE_USER': 'tutor1'}

    def test_submission_lifecycle(self):
        kw = dict(extra_environ=self.environ)
        url = '/events/demo/sheets/1/assignments/1/submit'

        response = app.get(url, **kw)
        ''':type response: webtest.TestResponse'''
        url = response.location
        assert url.endswith('/edit')
        url = url[len('http://localhost'):-len('/edit')]
        print url
        response = response.follow(**kw)

        ''':type response.form: webtest.Form'''
        response.form.set('filename', 'submission.txt')
        response.form.set('full_source', 'SourceCodeFromField')
        response.form.set('comment', '<b>Yo!</b><br><script>alert("buh");</script>')
        response = response.form.submit(**kw)
        response = response.follow(**kw)

        response = app.get(url + '/show', **kw)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('SourceCodeFromField', '<b>Yo!</b><br>',
            no=('SourceCodeFromFile', '<script>alert("buh");</script>'))

        response = app.get(url + '/edit', **kw)
        ''':type response.form: webtest.Form'''
        response = response.form.submit(upload_files=[('source_file', 'Submission.TXT', 'SourceCodeFromFile')], **kw)
        response = response.follow(**kw)

        response = app.get(url + '/show', **kw)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('SourceCodeFromFile',
            no=('SourceCodeFromField'))

        response = app.get(url + '/public', **kw)

        response = app.get(url + '/show', extra_environ={'REMOTE_USER': 'studenta1'})

        response = app.get(url + '/public', **kw)

        response = app.get(url + '/judge', **kw)
        ''':type response.form: webtest.Form'''
        response.form.set('comment', 'NopeThisIsNotReallyOkay<br><script>alert("buh");</script>')
        response.form.set('corrected_source', 'CorrectedCode')
        response.form.set('grade', '0.42')
        response = response.form.submit(**kw)
        response = response.follow(**kw)

        response = app.get(url + '/show', **kw)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('CorrectedCode', 'NopeThisIsNotReallyOkay<br>', '0.42',
            no=('<script>alert("buh");</script>'))

        response = app.get(url + '/edit', **kw)
        ''':type response.form: webtest.Form'''
        response = response.form.submit(upload_files=[('source_file', 'Submission.TXT', cyrillic_stuff)], **kw)

        response = app.get(url + '/edit', **kw)
        ''':type response.form: webtest.Form'''
        response = response.form.submit(upload_files=[('source_file', 'Submission.TXT', cyrillic_stuff+greek_stuff+chinese_stuff+japanese_stuff)], **kw)

        response = app.get(url + '/delete', **kw)

        response = app.get(url + '/show', status=status.HTTP_404_NOT_FOUND, **kw)
