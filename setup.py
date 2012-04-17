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

testpkgs=['WebTest >= 1.2.3',
               'nose',
               'coverage',
               'wsgiref',
               'repoze.who-testutil >= 1.0.1',
               ]
install_requires=[
    "TurboGears2 >= 2.1.5",
    "Mako",
    "Genshi", # For tgext.admin, see Ticket 143: https://sourceforge.net/p/turbogears2/tickets/143/
    "zope.sqlalchemy >= 0.4",
    "repoze.tm2 >= 1.0a5",
    "sqlalchemy >= 0.7",
    "repoze.what >= 1.0.8",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.what-pylons >= 1.0",
    "repoze.who==1.0.19",
    "tgext.admin >= 0.3.11",
    "repoze.what-quickstart",
    "repoze.what.plugins.sql>=1.0.1",
    "tw.forms",
    "tw.dynforms",
    "ipython==0.10.2", # For paster shell which I use heavily
    "Pygments", # For syntax highlighting
    "tgext.admin",
    "tgext.debugbar", # Dynamic debugging toolbar on every page
    #"tgext.menu",
    #"tgext.datahelpers", # For storing data as files, propably
    "tw.tinymce", # Javascript HTML editor
    "sprox", # Dynamic form widget generation
    #"tw.dojo" # Dynamic widgets using Javascript, renders TableForm too ugly
    ]

if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib', 'pysqlite'])
    install_requires.extend(['hashlib', 'pysqlite'])

#print install_requires

setup(
    name='SAUCE',
    version='0.4',
    description='System for AUtomated Code Evaluation',
    long_description=open('README.txt').read(),
    author='Moritz Schlarb',
    author_email='mail@moritz-schlarb.de',
    url='https://github.com/moschlar/SAUCE',
    license='BSD 2-clause',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2'],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'sauce': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'sauce': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = sauce.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    dependency_links=[
        "http://www.turbogears.org/2.1/downloads/current/"
        ],
    zip_safe=False
)
