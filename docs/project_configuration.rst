
=====================
Project configuration
=====================

.. contents::
   :depth: 3


Introduction
============

Project configuration is made with the buildout configuration files. By default
there is only two `cfg` files; `buildout.cfg` and `dev.cfg`.

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

[buildout]
----------

+---------------+-------------------------------------------------------------+
| auto-checkout | List of modules sources to auto checkout                    |
+---------------+-------------------------------------------------------------+
| develop       | List of editable modules to install with develop            |
+---------------+-------------------------------------------------------------+
| eggs          | List of eggs to install (project requirements)              |
+---------------+-------------------------------------------------------------+
| index         | HTTP URL of pypi (default) or a pypi mirror                 |
+---------------+-------------------------------------------------------------+
| newest        | Check for new packages versions (default `false`)           |
+---------------+-------------------------------------------------------------+
| parts         | Buildout parts to run (ex: python, djangodev)               |
+---------------+-------------------------------------------------------------+
| versions      | Freeze eggs or sources to specific versions                 |
+---------------+-------------------------------------------------------------+

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

+---------------+------------------------------------------------------------+
| eggs          | Default:  `${buildout:eggs}`                               |
+---------------+------------------------------------------------------------+
| extra-paths   | Default: `${python:extra-paths}`                           |
+---------------+------------------------------------------------------------+
| settings      | Name of the django settings module (default `settings`)    |
+---------------+------------------------------------------------------------+
| wsgi          | Default: false                                             |
+---------------+------------------------------------------------------------+

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



