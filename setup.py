# -*- coding: utf-8 -*-
# quickstarted Options:
#
# sqlalchemy: True
# auth:       sqlalchemy
# mako:       True
#
#

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'wsgiref',
    'repoze.who-testutil >= 1.0.1',
    ]

install_requires = [
    "TurboGears2 >= 2.1.5",
    "Mako",
    "zope.sqlalchemy >= 0.4",
    "repoze.tm2 >= 1.0a5",
    "sqlalchemy >= 0.7",
    "repoze.what >= 1.0.8",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.what-pylons >= 1.0",
    "repoze.who == 1.0.19",
    "repoze.what-quickstart",
    "repoze.what.plugins.sql >= 1.0.1",
    "tw.forms",
    "tw.dynforms",
    #"tw.dojo" # Dynamic widgets using Javascript, renders TableForm too ugly
    "tgext.admin >= 0.5",
    "tgext.crud >= 0.5",
    "sprox", # Dynamic form widget generation
    "tw.tinymce3 >= 0.9", # Javascript HTML editor using TinyMCE 3.x
    "tw.autosize", # Automatically resizing TextAreas
    "tablesorter", # JS-sortable TableBase
    "ipython == 0.10.2", # For paster shell which I use heavily
    "Pygments", # For syntax highlighting
    "docutils", # For rendering documentation
    "chardet", # For submission file charset detection
    ]

if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib', 'pysqlite'])
    install_requires.extend(['hashlib', 'pysqlite'])

setup(
    name='SAUCE',
    version='0.5.4',
    description='System for AUtomated Code Evaluation',
    long_description=open('README.rst').read(),
    author='Moritz Schlarb',
    author_email='mail@moritz-schlarb.de',
    url='https://github.com/moschlar/SAUCE',
    license='BSD 2-clause',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'sauce': ['i18n/*/LC_MESSAGES/*.mo',
                            'templates/*/*',
                            'public/*/*']},
    message_extractors={'sauce': [('**.py', 'python', None),
                                  ('templates/**.mako', 'mako', None),
                                  ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = sauce.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    dependency_links=[
        "http://tg.gy/215/",
        # For tw.tinymce3, tw.autosize, tablesorter which I packaged myself
        "https://github.com/moschlar/SAUCE/downloads",
        # For tgext.crud>=0.5.1 atm
        #"http://unstable.tg.gy/20120515/tgext.crud-0.5.1.tar.gz"
        ],
    zip_safe=False
)
