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

+----------------+----------------------------------------------------------------+
| **Command**    | **Description**                                                |
+----------------+----------------------------------------------------------------+
| buildout       | Run buildout to build or rebuild your environment              |
+----------------+----------------------------------------------------------------+
| dbshell        | Run the database shell (alias for `django runserver`)          |
+----------------+----------------------------------------------------------------+
| dev            | Run the duke development environement                          |
+----------------+----------------------------------------------------------------+
| python         | Run the python environement                                    |
+----------------+----------------------------------------------------------------+
| runserver      | Run the dev server (alias for `django runserver`)              |
+----------------+----------------------------------------------------------------+
| shell          | Run a python shell* (alias for `django shell`)                 |
+----------------+----------------------------------------------------------------+
| syncdb         | Synchronize database (alias for `django syncdb`)               |
+----------------+----------------------------------------------------------------+
| init           | Create the duke environement (run buildout after using init)   |
+----------------+----------------------------------------------------------------+
| startproject   | Create a new django project                                    |
+----------------+----------------------------------------------------------------+
| customize      | Copy the config of duke to ~/.duke (see Customisation_)        |
+----------------+----------------------------------------------------------------+
| help           | Print all the commandes                                        |
+----------------+----------------------------------------------------------------+
* if ipython is install, ipython will be ruen instead of python

.. _customisation: