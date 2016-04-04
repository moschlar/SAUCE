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

#  Quickstarted Options:
#
#  sqlalchemy: True
#  auth:       sqlalchemy
#  mako:       True
#
#

# This is just a work-around for a Python 2.7 issue causing an
# interpreter crash at exit when trying to log an info message.
try:
    import logging  # @UnusedImport pylint:disable=unused-import
    import multiprocessing  # @UnusedImport pylint:disable=unused-import
except:
    pass

import os, sys

here = os.path.dirname(os.path.abspath(__file__))

from setuptools import setup, find_packages

assert sys.version_info[:2] in ((2, 6), (2, 7))

install_requires = [
    'TurboGears2 >= 2.3.8',
    'Babel',
    'Mako',
    'zope.sqlalchemy >= 0.4',
    'repoze.tm2 >= 1.0a5',
    'sqlalchemy >= 0.8.2',
    'alembic',
    'repoze.who < 2.0',
    'repoze.who.plugins.sa',
    'repoze.who-testutil',
    'repoze.who-friendlyform >= 1.0.4',
    'repoze.what >= 1.0.8',
    'repoze.what.plugins.sql >= 1.0.1',
    'repoze.what-pylons >= 1.0',
    'repoze.what-quickstart',
    'tw2.core >= 2.2.1.1',
    'tw2.forms >= 2.1.4.2',
    'tw2.sqla',
    'tw2.dynforms',
    'tw2.jquery',
    'tw2.bootstrap.forms >= 2.2.2.1',
    'tw2.wysihtml5 >= 0.3.1',
    'tw2.jqplugins.chosen >= 0.3',
    'tw2.codemirror >= 0.2.1',
    'tw2.pygmentize >= 0.2.1',
    'tgext.admin >= 0.6.1, < 0.7',
    'tgext.crud >= 0.7, < 0.8',
    'sprox >= 0.9',  # Dynamic form widget generation
    'docutils',  # For rendering documentation
    'chardet',  # For submission file charset detection
    'bootalchemy >= 0.4.1',
    'repoze.sendmail',
    'bleach',
    'WebHelpers',
    'python-status',
]
if sys.version_info[:2] != (2, 7):
    install_requires += ['ordereddict']
tests_require = [
    'tg.devtools >= 2.3.8',
    'WebTest >= 1.2.3, < 2.0',
    'nose',
    'nose-exclude',
    'coverage',
    'gearbox',
    'wsgiref',
    'repoze.who-testutil >= 1.0.1',
    'BeautifulSoup',
    'sieve',  # tw2.core.testbase
    # 'tw2.core[tests]',
]
if sys.version_info[:2] != (2, 7):
    tests_require += ['unittest2']

extras_require = {
    'similarity': [
        'numpy',
        'matplotlib',
        'libripoff >= 0.2',
    ],
    'test': tests_require,
    'tests': tests_require,
    'nose': tests_require,
    'nosetests': tests_require,
    'sentry': ['raven'],
    'shell': ['ipython'],
    'lti': [
        'BeautifulSoup',
        'oauth2',
    ],
}

setup(
    name='SAUCE',
    version='1.8.0',
    description='System for AUtomated Code Evaluation',
    long_description=open(os.path.join(here, 'README.rst')).read(),
    author='Moritz Schlarb',
    author_email='sauce@moritz-schlarb.de',
    url='https://github.com/moschlar/SAUCE',
    license='AGPL-3.0',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    extras_require=extras_require,
    test_suite='nose.collector',
    tests_require=tests_require,
    package_data={'sauce': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'sauce': [
        ('**.py', 'python', None),
        ('templates/**.mako', 'mako', None),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = sauce.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ],
    },
    zip_safe=False,
)
