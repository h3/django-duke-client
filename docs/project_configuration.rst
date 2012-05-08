
=====================
Project configuration
=====================

.. contents::
   :depth: 3


Introduction
============

Project configuration is made with the buildout configuration files. By default
there is only two `cfg` files; `buildout.cfg` and `dev.cfg`.

It is possible to create stage specific configuration by adding `cfg` files named
after the stage name which extends `buildout.cfg`. 

For example, if I have a stage named `prod` on which I want to configure cron jobs, 
I simply have to create a `prod.cfg` file in which I put the required configuration.

At deploy time, duke will use `prod.cfg` instead of `buildout.cfg`.


buildout.cfg
------------

The main configuration is `buildout.cfg`, it should be complete and functional 
stand alone as this is the configuration used in production.


dev.cfg
-------

This configuration file is used only for development, it extends `buildout.cfg`.

You can extend individual configurations keys like so::

    [buildout]
    extends = buildout.cfg

    # extend
    eggs += 
     ipython

If you wish to overwrite it instead, simply remove the `+` sign.


Configurations
==============


[duke]
------

+----------------+-----------------------------------------+----------------------------------------+
| Directive      | Default                                 | Description                            |
+================+=========================================+========================================+
| django         | ${buildout:directory}/.duke/bin/django  | Shortcut to django executable          |
+----------------+-----------------------------------------+----------------------------------------+
| cron           | ${buildout:directory}/cron/             | Path where cron jobs script are stored |
+----------------+-----------------------------------------+----------------------------------------+


[buildout]
----------

+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| Directive                       | Default                 | Description                                                                |
+=================================+=========================+============================================================================+
| allowed-eggs-from-site-packages | PIL, MySQL-python, ...  | Use this directive to tell buildout which system wide package it can use*  |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| auto-checkout                   | djangodukerecipe        | List of modules sources to auto checkout                                   |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| develop                         | .                       | List of editable modules to install with develop                           |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| eggs                            | none                    | List of eggs to install (project requirements)                             |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| exec-sitecustomize              | false                   | Normally the Python's real sitecustomize module is not processed           |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| extensions                      | mr.developer            | Buildout extensions to load                                                |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| include-site-packages           | true                    | We allow site packages unless allowed-eggs-from-site-packages is specified |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| index                           | http://pypi.python.org  | HTTP URL of pypi (default) or a pypi mirror                                |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| newest                          | false                   | Check for new packages versions                                            |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| parts                           | python, django, scripts | Buildout parts to run (ex: python, djangodev)                              |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| unzip                           | true                    | Zipped eggs make debugging more difficult and often import more slowly     |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+
| versions                        | versions                | Freeze eggs or sources to specific versions                                |
+---------------------------------+-------------------------+----------------------------------------------------------------------------+

* If allowed-eggs-from-site-packages is an empty list, then no eggs from site-packages are chosen, but site-packages will still be included at the end of path lists.


[python]
--------

+---------------+-------------------------------------------------------------+
| interpreter   | Name of the Python interpreter (default `python`)           |
+---------------+-------------------------------------------------------------+
| extra-paths   | List of paths to add to the PYTHONPATH. Note that you must  |
|               | add paths of modules installed from sources here. The path  |
|               | should look like this: `${buildout:directory}/src/mptt`     |
+---------------+-------------------------------------------------------------+


[django]
--------

+---------------+-------------------------+------------------------------------+
| Directive     | Default                 | Description                        |
+===============+=================+=======+====================================+
| extra-paths   | `${python:extra-paths}` |                                    |
+---------------+-------------------------+------------------------------------+
| settings      | `settings`              | Name of the django settings module |
+---------------+-------------------------+------------------------------------+
| wsgi          | false                   |                                    |
+---------------+-------------------------+------------------------------------+
| project       | false                   | The project name                   |
+---------------+-------------------------+------------------------------------+


[sources]
--------

Example::

    [sources] # svn, hg or git                                                    
    django = git git://github.com/django/django.git
    django-mptt = git git://github.com/django-mptt/django-mptt.git


[versions]
----------

Example::

    [versions]
    django=1.4
    PIL=1.7.1


Working with sources
====================

If you work with source packages You need to edit tree configs.

Tell buildout to checkout the package every time::

    [buildout]
    auto-checkout += 
     django

Then specify the source URL::

    [sources] # svn, hg or git                                                    
    django = git git://github.com/django/django.git


Finally, add it to the environment's `PYTHONPATH` like this::

    [python]
    extra-paths +=
     ${buildout:directory}/src/django



