Test configuration
==================

Specifying the correct test parameters is probably the most
important and difficult task for a teacher user.

Therefore, this documentation seeks to explain **how** the
tests work and **how** to correctly configure them.

How tests work
--------------

Every time a *Submission* is changed and someone accesses the
``/results`` page, all associated *Tests* are run and the *Testruns* are
saved and displayed. This also affects the state *result*
of the *Submission*.

A *Test* has an attribute ``visibility``. The setting controls whether
expected test output on the *Assignment* page and how the *Testrun* results
are shown to the user.

How to configure tests
----------------------

When configuring a *Test* case there are many options available in the administration panel:

Running options
^^^^^^^^^^^^^^^

+-------------------------+------------------+---------------------------------+
| Option                  | Type /           | Description                     |
|                         | Default          |                                 |
+=========================+==================+=================================+
| ``visibility``          | Enum             | Depending on this setting,      |
|                         |                  | expected test results are shown |
|                         | ``invisible``,   | on the *Assignment* page and/or |
|                         | ``result_only``, | *Testrun* results are shown     |
|                         | ``data_only``,   | with their data, with result,   |
|                         | ``visible``      | both, or not at all.            |
|                         |                  |                                 |
+-------------------------+------------------+---------------------------------+
| ``timeout``             | Float            | Maximum runtime of test process.|
|                         |                  |                                 |
|                         | None             | If not set, the value from the  |
|                         |                  | *Assignment* will be used or no |
|                         |                  | time limit at all is applied.   |
+-------------------------+------------------+---------------------------------+
| ``argv``                | String           | Command line arguments for test |
|                         |                  | program run                     |
|                         | None             |                                 |
|                         |                  | Possible variables are:         |
|                         |                  |                                 |
|                         |                  | :``{path}``:                    |
|                         |                  |     Absolute path to            |
|                         |                  |     temporary working directory |
|                         |                  | :``{infile}``:                  |
|                         |                  |     Full path to test           |
|                         |                  |     input file                  |
|                         |                  | :``{outfile}``:                 |
|                         |                  |     Full path to test           |
|                         |                  |     output file                 |
|                         |                  |                                 |
+-------------------------+------------------+---------------------------------+
| ``input_type`` /        | Enum             | If set, any line starting with  |
| ``output_type``         |                  | ``comment_prefix`` will be      |
|                         | ``stdin``,       | ignored in the test validation  |
|                         | ``stdout``       |                                 |
|                         |                  |                                 |
+-------------------------+------------------+---------------------------------+
| ``input_filename`` /    | String           | If set, any line starting with  |
| ``output_filename``     |                  | ``comment_prefix`` will be      |
|                         | None             | ignored in the test validation  |
|                         |                  |                                 |
|                         |                  |                                 |
+-------------------------+------------------+---------------------------------+
| ``input_data`` /        | String           | If set, any line starting with  |
| ``output_data``         |                  | ``comment_prefix`` will be      |
|                         |                  | ignored in the test validation  |
|                         |                  |                                 |
|                         |                  |                                 |
+-------------------------+------------------+---------------------------------+


Validation options
^^^^^^^^^^^^^^^^^^^^^

+-------------------------+----------+---------------------------------+
| Option                  | Type /   | Description                     |
|                         | Default  |                                 |
+=========================+==========+=================================+
| ``ignore_case``         | Boolean  | To ignore the case of the       |
|                         |          | output, this simply calls       |
|                         | ``True`` | ``.lower()`` on the whole       |
|                         |          | output string before comparison |
+-------------------------+----------+---------------------------------+
| ``ignore_returncode``   | Boolean  | If ``False``, the *Test* will   |
|                         |          | only be considered successful,  |
|                         | ``True`` | if its process return code is   |
|                         |          | ``== 0``                        |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``comment_prefix``      | String   | If set, any line starting with  |
|                         |          | ``comment_prefix`` will be      |
|                         | ``'#'``  | ignored in the test validation  |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``show_partial_match``  | Boolean  | If set, if the observed output  |
|                         |          | matches the beginning of the    |
|                         | ``True`` | expected output, this partial   |
|                         |          | match will be displayed as such |
|                         |          | to the *User* to indicate a     |
|                         |          | possible timeout error.         |
+-------------------------+----------+---------------------------------+
| ``separator``           | String   | The separator string to use for |
|                         |          | ``.split()``, if set.           |
|                         | ``None`` | May contain a string as set of  |
|                         |          | characters on any of which the  |
|                         |          | output shall be splitted.       |
|                         |          |                                 |
|                         |          | If set to ``None`` (default),   |
|                         |          | splitting will be done on any   |
|                         |          | whitespace character            |
|                         |          | (Python default).               |
+-------------------------+----------+---------------------------------+
| ``splitlines``          | Boolean  | Split output by lines using the |
|                         |          | Python ``.splitlines()``        |
|                         | ``False``| function.                       |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``split``               | Boolean  | Split output by ``separator``.  |
|                         |          |                                 |
|                         | ``True`` | Applies to full output, if      |
|                         |          | ``splitlines`` is ``False``,    |
|                         |          | but to each line from           |
|                         |          | ``.splitlines()`` if            |
|                         |          | ``splitlines`` is ``True``.     |
+-------------------------+----------+---------------------------------+
| ``sort``                | Boolean  |                                 |
|                         |          |                                 |
|                         | ``False``|                                 |
|                         |          | Sort output before comparison.  |
|                         |          |                                 |
|                         |          | Parsing is performed first,     |
|                         |          | if enabled.                     |
|                         |          |                                 |
|                         |          | Results depends on              |
|                         |          | whether ``splitlines`` and/or   |
|                         |          | ``split`` are set:              |
|                         |          |                                 |
|                         |          | if ``split`` and ``splitlines``:|
|                         |          | 2-dimensional array in which    |
|                         |          | only the second dimension is    |
|                         |          | sorted (e.g.                    |
|                         |          | ``[[3, 4], [1, 2]])``           |
|                         |          |                                 |
|                         |          | if only ``split`` or only       |
|                         |          | ``splitlines``:                 |
|                         |          | 1-dimensional list is sorted    |
|                         |          | by the types default comparator |
+-------------------------+----------+---------------------------------+
| ``parallel_sort``       | Boolean  |                                 |
|                         |          |                                 |
|                         | ``False``|                                 |
|                         |          | Sort output by an integer value |
|                         |          | within square brackets ``[]``.  |
|                         |          | Useful for assignments in       |
|                         |          | courses of parallel             |
|                         |          | programming.                    |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``parse_int``           | Boolean  | Parse every substring in output |
|                         |          | to ``int`` before comparison.   |
|                         | ``False``|                                 |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``parse_float``         | Boolean  | Parse every substring in output |
|                         |          | to ``float`` before comparison. |
|                         | ``False``|                                 |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``float_precision``     | Float    | The precision (number of        |
|                         |          | decimal digits) to compare      |
|                         | ``None`` | for floats                      |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
