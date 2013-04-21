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

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

assert sys.version_info[:2] in ((2, 6), (2, 7))


install_requires = [
    "TurboGears2 >= 2.1.4, <= 2.2.2",
    "Mako",
    "zope.sqlalchemy >= 0.4",
    "repoze.tm2 >= 1.0a5",
    "sqlalchemy >= 0.7, <= 0.7.99",
    "alembic",
    "repoze.who <= 1.99", # Just to not get 2.0
    "repoze.who.plugins.sa",
    "repoze.who-testutil",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.what >= 1.0.8",
    "repoze.what.plugins.sql >= 1.0.1",
    "repoze.what-pylons >= 1.0",
    "repoze.what-quickstart",
    "tw2.core == 2.1.3",
    "tw2.forms >= 2.1.1, < 2.1.4",
    "tw2.dynforms",
    "tw2.jquery",
    "tw2.bootstrap.forms",
    "tw2.tinymce > 2.0.b4",
    "tw2.jqplugins.chosen",
    "tw2.ace",
    "tgext.admin >= 0.5.3",
    "tgext.crud >= 0.5.6",
    "sprox >= 0.8",  # Dynamic form widget generation
#    "tablesorter >= 0.2",  # JS-sortable TableBase
#    "ipython == 0.10.2",  # For paster shell, install by hand if necessary
    "Pygments",  # For syntax highlighting
    "docutils",  # For rendering documentation
    "chardet",  # For submission file charset detection
    "pygmentize > 0.2",  # Using ToscaWidgets with a SyntaxHighlighting widget
    "bootalchemy >= 0.4.1",
#    "WebOb <= 1.1.1, >= 1.0.8", "Pylons == 1.0",  # To allow one-step installing
#    "tg.devtools >= 2.1.4, <= 2.2.2",
    ]
extras_require = {
    'similarity': [
        "numpy",
        "matplotlib",
        "libripoff >= 0.2",
    ],
}
tests_require = [
    'WebTest >= 1.2.3',
    'nose',
    'nose-exclude',
    'coverage',
    'wsgiref',
    'repoze.who-testutil >= 1.0.1',
    'BeautifulSoup',
    sys.version_info[:2] != (2, 7) and 'unittest2' or '',
    ]

setup(
    name='SAUCE',
    version='1.3',
    description='System for AUtomated Code Evaluation',
    long_description=open('README.rst').read(),
    author='Moritz Schlarb',
    author_email='sauce@moritz-schlarb.de',
    url='https://github.com/moschlar/SAUCE',
    license='AGPL-3.0',
    setup_requires=["PasteScript >= 1.7"],
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
    entry_points="""
    [paste.app_factory]
    main = sauce.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    dependency_links=[
        "http://tg.gy/current/",
        #TODO: Get rid of these
        "https://github.com/moschlar/tw2.ace/archive/master.tar.gz#egg=tw2.ace-0.1dev",
        "https://bitbucket.org/percious/bootalchemy/get/0.4.1.tar.gz#egg=bootalchemy-0.4.1",
        "https://github.com/moschlar/SAUCE/downloads",
        ],
    zip_safe=False
)
