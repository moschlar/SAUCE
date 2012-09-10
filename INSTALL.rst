==============================================
 SAUCE - System for AUtomated Code Evaluation
==============================================


Usage
-----

Once a WSGI server has started the SAUCE application
(see below for instructions) you should have gotten
some default dummy data (Events, Assignments, Submissions,
Students). 

For login data please see README.rst.


Installation and Setup
----------------------


Development Setup
^^^^^^^^^^^^^^^^^

First, if not already installed, install virtualenv::

    $ easy_install virtualenv

Then create a virtualenv and source the activate script::

    $ virtualenv --no-site-packages tg
    $ cd tg
    $ . bin/activate

Now install Turbogears::

    $ easy_install -i http://tg.gy/current tg.devtools

Then checkout the SAUCE repository::

    $ git clone https://github.com/moschlar/SAUCE.git
    $ cd SAUCE
    $ git submodule init && git submodule update

And resolve all additional dependencies::

    $ python setup.py develop

Now setup the required database tables and pre-fill them
with some dummy data::

    $ paster setup-app development.ini

To start the development webserver use the command::

    $ paster serve development.ini

While developing you may want the server to reload after changes in
package files (or its dependencies) are saved.
This can be achieved easily by adding the --reload option::

    $ paster serve --reload development.ini

Then you are ready to go.
