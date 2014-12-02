==================
django-duke-client
==================

Django duke client aims provide a turnkey development environment for django 
and make django development easier and faster.

It is currently built for the new project layout of django 1.4. The older 
project layout support might be implemented someday, but right now it's not
a priority.

Official documentation: http://readthedocs.org/docs/django-duke-client/en/latest/

Requirement
===========

.. code-block:: bash

    $ sudo apt-get install python-yaml



Installation
============

We're still in early development so it's suggested to install it from source
using `develop` instead of install:

.. code-block:: bash

   $ git clone git://github.com/h3/django-duke-client.git
   $ cd django-duke-client/
   $ sudo python setup.py develop

To update it:

.. code-block:: bash

   $ cd django-duke-client/
   $ git pull
   $ sudo python setup.py develop

Usage
=====

for the impatients
^^^^^^^^^^^^^^^^^^

Create and build a project:

.. code-block:: bash

    user@host$ duke startproject test-project
    user@host$ cd test-project/
    user@host$ duke init testproject
    user@host|testproject:~/.../trunk/test-project$ buildout

Note:
 "test-project" must not contain any dots "."

Start working:

.. code-block:: bash

    user@host|testproject:~/.../trunk/test-project$ cd testproject/
    user@host|testproject:~/.../trunk/test-project$ django syncdb
    user@host|testproject:~/.../trunk/test-project$ django runserver

Tutorials
^^^^^^^^^

* Official getting started tutorial_

.. _tutorial: http://readthedocs.org/docs/django-duke-client/en/latest/tutorial.html
