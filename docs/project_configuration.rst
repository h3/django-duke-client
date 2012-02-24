
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

This is the base configuration file. It should contain only stage independant 
(global) configs.

dev.cfg
-------

This configuration file is used only for development, it extends `buildout.cfg`.

You can also extend or overwrite individual configurations like so::

    [buildout]
    extends = buildout.cfg

    # extend
    eggs += 
     ipython

If you wish to overwrite instead, simply remove the `+` sign.


Configurations
==============

[buildout]
----------

+---------------+------------------------------------------------+
| auto-checkout |                                                |
+---------------+------------------------------------------------+
| develop       |                                                |
+---------------+------------------------------------------------+
| eggs          |                                                |
+---------------+------------------------------------------------+
| newest        |                                                |
+---------------+------------------------------------------------+
| parts         |                                                |
+---------------+------------------------------------------------+
| versions      |                                                |
+---------------+------------------------------------------------+

[python]
--------

+---------------+-----------------------------------------------+
| extra-paths   |                                               |
+---------------+-----------------------------------------------+

[djangodev] & [djangoprod]
--------------------------

+---------------+-----------------------------------------------+
| eggs          |                                               |
+---------------+-----------------------------------------------+

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



