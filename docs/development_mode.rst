================
Development mode
================

.. contents::
   :depth: 3


Introduction
============

One of the key feature of django duke is to provide a sandboxed development
environment which provide some shortcuts and utilities to make it easier to 
work with django.

To activate the development environment on a project managed by duke, simply
go in the project folder and type `duke dev`::

    $: cd my-project-name/
    $: duke dev
    (my-project-name) $:

Once the development environment is activated, the shell prompt should be 
prefixed with the project's name to indicate that you are working within
a sandboxed environment.

The distinction is important because the development environment extends 
your shell with new commands and does some magic to make sure you are 
working within the sandbox.

For example, if you type the command `python` in dev mode, the Python 
interpreter executed isn't the system wide python interpreter (usually 
`/usr/bin/python`). Instead it will call the python interpreter sandboxed
in `my-project-name/.duke/bin/python`.

The environment also provide shortcuts and commands to ease the development
process.

Commands & shortcuts
====================

+------------+----------------------------------------------------------------+
| Command    | Description                                                    |
+------------+----------------------------------------------------------------+
| buildout   | Run buildout to build or rebuild your environment              |
+------------+----------------------------------------------------------------+
| deactivate | Deactivates the development environment.                       |
+------------+----------------------------------------------------------------+
| develop    | Use this to install, activate or deactivate python packages.   |
+------------+----------------------------------------------------------------+
| django     | Use this instead of manage.py                                  |
+------------+----------------------------------------------------------------+
| python     | A sandboxed python interpreter \*                              |
+------------+----------------------------------------------------------------+
| run_tests  | Runs the django test suite                                     |
+------------+----------------------------------------------------------------+

\* If IPython is installed, it will be used by default when working in the env.
