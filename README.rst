==============================================
 SAUCE - System for AUtomated Code Evaluation
==============================================

A web based system for automatic code evaluation in the 
context of programming courses and contests.

This software project is licensed under the
``BSD 2-clause`` license. You find a copy of that 
license in the file
`LICENSE.txt <https://github.com/moschlar/SAUCE/blob/develop/LICENSE.txt>`_.

:Build status:
  .. image:: https://secure.travis-ci.org/moschlar/SAUCE.png?branch=develop
  
  `Details <http://travis-ci.org/moschlar/SAUCE>`_

For installation instructions, see
`INSTALL.rst <https://github.com/moschlar/SAUCE/blob/develop/INSTALL.rst>`_.


Demo instance
=============

If you want to try out SAUCE, you can access the demo instance
at http://demo1-sauce.rhcloud.com/ .

The instance has some dummy data which includes several users and
a sample event called ``eip12``: http://demo1-sauce.rhcloud.com/events/eip12

You can `log in <http://demo1-sauce.rhcloud.com/login>`_
for different roles using the following credentials:

+--------------------+----------------+-----------------+-------------------------------------------------------------------+
| Role               | Username       | Password        | What's special to see with this role?                             |
+====================+================+=================+===================================================================+
| Master teacher     | ``teacher``    | ``teachpass``   | The event administration page at                                  |
| (responsible for   |                |                 | http://demo1-sauce.rhcloud.com/events/eip12/admin                 |
| event ``eip12``)   |                |                 | and the lesson submission page at                                 |
|                    |                |                 | http://demo1-sauce.rhcloud.com/events/eip12/lessons/2/submissions |
|                    |                |                 | and the judgement pages for the submissions.                      |
+--------------------+----------------+-----------------+-------------------------------------------------------------------+
| Assistant teacher  | ``teacherass`` | ``teachpass``   | The lesson submission page at                                     |
| (responsible for   |                |                 | http://demo1-sauce.rhcloud.com/events/eip12/lessons/1/submissions |
| lesson 1 of event  |                |                 | and the judgement pages for the submissions.                      |
| ``eip12``)         |                |                 |                                                                   |
+--------------------+----------------+-----------------+-------------------------------------------------------------------+
| Various students   | ``studenta1``, | ``studentpass`` | The user profile page, where you can see your own                 |
| of event ``eip12`` | ``studenta2``, |                 | and your team member's submissions at                             |
|                    | ``studentb1``, |                 | http://demo1-sauce.rhcloud.com/user                               |
|                    | ``studentc1``, |                 |                                                                   |
|                    | ``studentc2``  |                 |                                                                   |
+--------------------+----------------+-----------------+-------------------------------------------------------------------+

