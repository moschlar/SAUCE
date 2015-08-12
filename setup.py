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
# quickstarted Options:
#
# sqlalchemy: True
# auth:       sqlalchemy
# mako:       True
#

# Fix shutdown errors while installing
try:
    import multiprocessing  # @UnusedImport
    import logging  # @UnusedImport
except:
    pass

import os, sys

here = os.path.dirname(os.path.abspath(__file__))

from setuptools import setup, find_packages

assert sys.version_info[:2] in ((2, 6), (2, 7))

install_requires = [
    'TurboGears2 >= 2.2.0, <= 2.2.2',
    'Mako',
    'zope.sqlalchemy >= 0.4',
    'repoze.tm2 >= 1.0a5',
    'sqlalchemy >= 0.7, < 0.9',
    'alembic',
    'repoze.who <= 1.99',  # Just to not get 2.0
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
    'tw2.bootstrap.forms >= 2.2.0',
    'tw2.wysihtml5 >= 0.3.1',
    'tw2.jqplugins.chosen >= 0.3',
    'tw2.ace >= 0.2.1',
    'tw2.pygmentize >= 0.2.1',
    'tgext.admin >= 0.6',
    'tgext.crud >= 0.7',
    'sprox >= 0.9',  # Dynamic form widget generation
    'docutils',  # For rendering documentation
    'chardet',  # For submission file charset detection
    'bootalchemy >= 0.4.1',
    'repoze.sendmail',
]
if sys.version_info[:2] != (2, 7):
    install_requires += ['ordereddict']
tests_require = [
    'WebTest >= 1.2.3',
    'nose',
    'nose-exclude',
    'coverage',
    'wsgiref',
    'repoze.who-testutil >= 1.0.1',
    'BeautifulSoup',
    'sieve',  # tw2.core.testbase
]
if sys.version_info[:2] != (2, 7):
    tests_require += ['unittest2']

extras_require = {
    'similarity': [
        'numpy',  # Maybe needs to be installed beforehand
        'matplotlib',
        'libripoff >= 0.2',
    ],
    'test': tests_require,
    'tests': tests_require,
    'nose': tests_require,
    'nosetests': tests_require,
    'sentry': ['raven'],
    'shell': ['ipython == 0.10.2'],
    'lti': [
        'BeautifulSoup',
        'oauth2',
    ],
}

setup(
    name='SAUCE',
    version='1.7.4',
    description='System for AUtomated Code Evaluation',
    long_description=open(os.path.join(here, 'README.rst')).read(),
    author='Moritz Schlarb',
    author_email='sauce@moritz-schlarb.de',
    url='https://github.com/moschlar/SAUCE',
    license='AGPL-3.0',
    setup_requires=['PasteScript >= 1.7'],
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    test_suite='nose.collector',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={'sauce': ['i18n/*/LC_MESSAGES/*.mo',
                            'templates/*/*',
                            'public/*/*']},
    message_extractors={'sauce': [('**.py', 'python', None),
                                  ('templates/**.mako', 'mako', None),
                                  ('public/**', 'ignore', None)]},
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    entry_points='''
    [paste.app_factory]
    main = sauce.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    ''',
    dependency_links=[
        'http://tg.gy/current/',
    ],
    zip_safe=False,
)
