==============================================
 SAUCE - System for AUtomated Code Evaluation
==============================================


Usage
-----

Once a WSGI server has started the SAUCE application
(see below for instructions) you should have gotten
some default dummy data (Events, Assignments, Submissions,
Users).

For login data please see README.rst.


Installation and Setup
----------------------


Development Setup
^^^^^^^^^^^^^^^^^

To set up a local instance of the SAUCE application, you will need:

- An UNIX-like operating system
- A Python interpreter (2.6 or 2.7)
- The ``virtualenv`` package for Python
  (e.g. called ``python-virtualenv`` in Ubunutu 12.04)
- The Python packages ``numpy`` and ``matplotlib`` have to be
  installed system-wide, too.
  (e.g. called ``python-numpy`` and ``python-matplotlib`` in
  Ubunutu 12.04)

No further packages have to be installed in the system, everything else
gets installed inside a virtualenv (a "sandbox" for installing Python
packages without polluting the system ``site-packages``).

Now create such a virtualenv and source the ``activate`` script to
enter it (the option ``--system-site-packages`` is important to
make the ``numpy`` and ``matplotlib`` packages available inside the
virtualenv)::

    $ virtualenv --system-site-packages tg
    $ cd tg
    $ . bin/activate

Now checkout the SAUCE repository::

    $ git clone https://github.com/moschlar/SAUCE.git
    $ cd SAUCE
    $ git submodule init && git submodule update

Then install SAUCE and all additional dependencies::

    $ python setup.py develop

Now setup the required database tables and pre-fill them
with some dummy data::

    $ paster setup-app development.ini

To start the development webserver use the command::

    $ paster serve development.ini

While developing you may want the server to reload after any source
code file is changed.
This can be achieved easily by adding the ``--reload`` option::

    $ paster serve --reload development.ini

Then you are ready to go.
You can access your instance of the application by browsing to:
http://localhost:8080/


Test suite
^^^^^^^^^^

To execute the test suite, simply run::

    $ nosetests
