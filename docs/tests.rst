Test configuration
==================

Specifying the correct test parameters is probably the most important and difficult task for a teacher user.

Therefore, this documentation seeks to explain **how** the tests work and **how** to correctly configure them.

How tests work
--------------

Basically, there are two types of *Tests* and two types of *Testruns*.

A *Test* has a boolean attribute ``visible``. 

    Only if ``visible`` is set to ``True``, the test input and the expected test output are shown to the user on the *Assignment* page.

Different types of *Testruns* are performed when different buttons are clicked on the *Submission* page:

-  *Testruns* performed after clicking Test are not saved to the database, their output is only once rendered for the submitter while editing his *Submission*.

-  *Testruns* performed after clicking Submit are saved to the database and available for later displaying.

The buttons on the *Submission* page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On the *Submission* edit page, there are three buttons: 
Test, Finish and Delete.
Their functionality explained in detail:

**Test**
    When the *User* has entered his *Submission* source code or selected a file to upload and clicks on the Test button, the *Submission* is saved to the database and all visible *Tests* associated with the *Assignment* are run. 

    For each test, the test input, expected and observed output and error output (if any) are displayed (for convenience, a diff is displayed when the test run was not successful).

    Only if all visible *Tests* ran successfully, the Finish button is enabled.

**Finish**
    When the *User* clicks the Finish button, the *Submission* is marked as ``completed`` and cannot be edited anymore. Then all *Test* cases (visible and non-visible) are run on the *Submission* and their respective output and error data as well as their result after validation get saved to the database for future displaying.

    The Finish button is only enabled, when the *User* has previously tested his submission successfully. While this prevents *Student*, *Teacher* and the system from running lots of presumably failing *Test* cases on the *Submission*, it still ensures that the *Submission* source code is safely stored to the database and the *Teacher* can see and grade the failed attempt. 
    Also, the *Teacher* can override this convention and run the non-visible *Tests* to see if the *Submission* is just missing some corner-cases.

**Delete**
    When the Delete button is clicked, the *Submission* is deleted from the database. The *User* gets redirected to the corresponding *Assignment* page of the *Submission* he just deleted.

How to configure tests
----------------------

When configuring a *Test* case there are many options available in the administration panel:

Running options
^^^^^^^^^^^^^^^

+-------------------------+----------+---------------------------------+
| Option                  | Type /   | Description                     |
|                         | Default  |                                 |
+=========================+==========+=================================+
| ``visible``             | Boolean  | If set, the *Test* is shown to  |
|                         |          | users on the *Assignment* page  |
|                         | ``False``| and it is run when the Test     |
|                         |          | button is clicked.              |
+-------------------------+----------+---------------------------------+
| ``timeout``             | Float    | Maximum runtime of test process.|
|                         |          |                                 |
|                         | None     | If not set, the value from the  |
|                         |          | *Assignment* will be used or no |
|                         |          | time limit at all is applied.   |
+-------------------------+----------+---------------------------------+
| ``argv``                | String   | Command line arguments for test |
|                         |          | program run                     |
|                         | None     |                                 |
|                         |          | Possible variables are:         |
|                         |          |                                 |
|                         |          | :``{path}``:                    |
|                         |          |     Absolute path to            |
|                         |          |     temporary working directory |
|                         |          | :``{infile}``:                  |
|                         |          |     Full path to test           |
|                         |          |     input file                  |
|                         |          | :``{outfile}``:                 |
|                         |          |     Full path to test           |
|                         |          |     output file                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``input_type`` /        |Enum      | If set, any line starting with  |
| ``output_type``         |          | ``comment_prefix`` will be      |
|                         |``stdin``/| ignored in the test validation  |
|                         |``stdout``|                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``input_filename`` /    | String   | If set, any line starting with  |
| ``output_filename``     |          | ``comment_prefix`` will be      |
|                         | None     | ignored in the test validation  |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+
| ``input_data`` /        | String   | If set, any line starting with  |
| ``output_data``         |          | ``comment_prefix`` will be      |
|                         |          | ignored in the test validation  |
|                         |          |                                 |
|                         |          |                                 |
+-------------------------+----------+---------------------------------+


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






