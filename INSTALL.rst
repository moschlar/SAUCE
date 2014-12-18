Installation and Setup
----------------------

Development Setup
^^^^^^^^^^^^^^^^^

To set up a local instance of the SAUCE application, you will need:

- An UNIX-like operating system
- A Python interpreter (2.6 or 2.7)
- The ``virtualenv`` package for Python
  (e.g. called ``python-virtualenv`` in Ubuntu)
  
*Optionally*, you can:

- Install the Python packages ``numpy`` and ``matplotlib``
  from your distribution (e.g. called ``python-numpy`` and
  ``python-matplotlib`` in  Ubuntu), which will save you some time
  and hassle if they don't have to be compiled.
  
  **NOTE:** If you do this, you will have to create your virtualenv
  below with ``--system-site-packages`` instead of ``--no-site-packages``.
  If you are not familiar with what this switch does, please ask
  for help *now* to avoid problems in the future ;).

No further packages have to be installed in the system, everything else
gets installed inside a `virtualenv <http://www.virtualenv.org>`_
(a "sandbox" for installing Python packages without polluting the systems
``site-packages``).

Now create such a virtualenv and source the ``activate`` script to
enter it.
(Remember to use ``--system-site-packages`` if you want to
make the ``numpy`` and ``matplotlib`` packages installed through your
distribution available inside the virtualenv)::

    $ virtualenv --no-site-packages tg
    $ cd tg
    $ . bin/activate

Now checkout the SAUCE repository::

    $ git clone https://github.com/moschlar/SAUCE.git
    $ cd SAUCE
    $ git submodule init && git submodule update

Then install SAUCE and all additional dependencies::

    $ pip install -i http://tg.gy/current tg.devtools
    $ pip install -e .

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

Usage
^^^^^

Once a WSGI server has started the SAUCE application
(see below for instructions) you should have gotten
some default dummy data (Events, Assignments, Submissions,
Users).

For login data please see README.rst.

Test suite
^^^^^^^^^^

To execute the test suite, simply run::

    $ python setup.py test
