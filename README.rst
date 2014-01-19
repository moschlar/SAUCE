==============================================
 SAUCE
==============================================
----------------------------------------------
 System for AUtomated Code Evaluation
----------------------------------------------

A web based system for automatic code evaluation in the 
context of programming courses and contests.

This software project is licensed under the
GNU Affero General Public License, Version 3 (AGPL-3.0).
You find a copy of that license in the file
`LICENSE.txt <https://github.com/moschlar/SAUCE/blob/develop/LICENSE.txt>`_.

.. image:: http://stillmaintained.com/moschlar/SAUCE.png
   :target: http://stillmaintained.com/moschlar/SAUCE
   :alt: Project Status

Build Status
============

.. |travis-master| image:: https://secure.travis-ci.org/moschlar/SAUCE.png?branch=master
   :target: http://travis-ci.org/moschlar/SAUCE
   :alt: Build Status - master branch

.. |travis-develop| image:: https://secure.travis-ci.org/moschlar/SAUCE.png?branch=develop
   :target: http://travis-ci.org/moschlar/SAUCE
   :alt: Build Status - develop branch

.. |coveralls-master| image:: https://coveralls.io/repos/moschlar/SAUCE/badge.png?branch=master
   :target: https://coveralls.io/r/moschlar/SAUCE?branch=master
   :alt: Test Coverage - master branch
   
.. |coveralls-develop| image:: https://coveralls.io/repos/moschlar/SAUCE/badge.png?branch=develop
   :target: https://coveralls.io/r/moschlar/SAUCE?branch=develop
   :alt: Test Coverage - develop branch

.. |landscape-master| image:: https://landscape.io/github/moschlar/SAUCE/master/landscape.png
   :target: https://landscape.io/github/moschlar/SAUCE/master
   :alt: Code Health - master branch

.. |landscape-develop| image:: https://landscape.io/github/moschlar/SAUCE/develop/landscape.png
   :target: https://landscape.io/github/moschlar/SAUCE/develop
   :alt: Code Health - develop branch

+--------------+------------------+---------------------+---------------------+
| Branch       | Build Status     | Test Coverage       | Code Health         |
+==============+==================+=====================+=====================+
| **master**   | |travis-master|  | |coveralls-master|  | |landscape-master|  |
+--------------+------------------+---------------------+---------------------+
| **develop**  | |travis-develop| | |coveralls-develop| | |landscape-develop| |
+--------------+------------------+---------------------+---------------------+


Installation
============

For installation instructions, see
`INSTALL.rst <https://github.com/moschlar/SAUCE/blob/develop/INSTALL.rst>`_.


Demo instance
=============

If you want to try out **SAUCE** without setting up your own instance,
you can access the demo instance at https://sauce-moschlar.rhcloud.com/
or https://sauce-moschlar.herokuapp.com/.

Every newly set up instance has some dummy data which includes several
users and a sample event called `Programming 101 - Demo`_.

You can `log in`_ for different user roles using the following credentials:

+----------------------+----------------+-----------------+---------------------------------------------------+
| Role                 | Username       | Password        | What's special to see with this role?             |
+======================+================+=================+===================================================+
| **Teacher**          | ``teacher1``,  | ``teachpass``   | The event administration page at                  |
| (responsible for an  | (``teacher2``) |                 | `/events/demo/admin`_                             |
| event - creating     |                |                 | and the lesson submission page at                 |
| sheets, assignments, |                |                 | `/events/demo/lessons/1/submissions`_             |
| tests, lessons,      |                |                 | and the judgement pages for the submissions.      |
| tutors, students,    |                |                 |                                                   |
| etc.)                |                |                 |                                                   |
+----------------------+----------------+-----------------+---------------------------------------------------+
| **Tutor**            | ``tutor1``,    | ``tutorpass``   | The lesson submission page at                     |
| (responsible for     | (``tutor2``)   |                 | `/events/demo/lessons/2/submissions`_             |
| a single lesson of   |                |                 | and the judgement pages for the submissions.      |
| an event)            |                |                 | Also, the similarity page for an assignment       |
|                      |                |                 | would be very interesting.                        |
+----------------------+----------------+-----------------+---------------------------------------------------+
| Various **Students** | ``studenta1``, | ``studentpass`` | The user profile page, where you can see your own |
| in different teams   | ``studenta2``, |                 | and your team members' submissions at             |
| and lessons and      | ``studenta3``, |                 | `/user`_                                          |
| events               | ``studentb1``, |                 |                                                   |
|                      | ``studentb2``, |                 |                                                   |
|                      | ``studentc1``, |                 |                                                   |
|                      | ``studentc2``, |                 |                                                   |
|                      | ``studentd1``, |                 |                                                   |
|                      | ``studentd2``, |                 |                                                   |
|                      | ``studentd3``, |                 |                                                   |
|                      | ``studente1``  |                 |                                                   |
+----------------------+----------------+-----------------+---------------------------------------------------+

.. _Programming 101 - Demo: https://sauce-moschlar.rhcloud.com/events/demo
.. _log in: https://sauce-moschlar.rhcloud.com/login
.. _/user: https://sauce-moschlar.rhcloud.com/user
.. _/events/demo/admin: https://sauce-moschlar.rhcloud.com/events/demo/admin
.. _/events/demo/lessons/2/submissions: https://sauce-moschlar.rhcloud.com/events/demo/lessons/2/submissions
.. _/events/demo/lessons/1/submissions: https://sauce-moschlar.rhcloud.com/events/demo/lessons/1/submissions
