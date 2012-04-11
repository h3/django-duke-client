========
Tutorial
========

.. contents::
   :depth: 3

Project layout
==============

The django duke client tries to be independent as possible in term of project layout. However a minimal structure is
required for it to work properly.

This is the absolute minimal project layout to initialize duke::

    project-root-folder/
      - setup.py

When the project is built, it looks like this::

    project-root-folder/
      - bootstrap.py
      - buildout.cfg
      - dev.cfg
      - setup.py
      + .duke/
        + bin/
        + develop-eggs/
        + eggs/
        + parts/
      + projectname.egg-info
      + src/
      + projectname/
        - settings.py
        - local_settings.py
        + conf/
            + settings/
                - default.py
                - dev.py

Starting a project from scratch
===============================

Creating a new project from scratch is easy as::

    user@host$ duke startproject my-project-name
    user@host$ cd my-project-name/
    user@host$ ls
    README.rst  setup.py

The `setup.py` file is the only required file for a new project. The
README.rst is created only for convenience. The next step is to edit
the setup file according to your needs.

Initializing your project
=========================

Next we need to initialize duke on this project. Which can be done
like so::

    user@host$ duke init myprojectname
    Installing bootstrap.py..
    Installing default buildout.cfg
    Installing default base.cfg
    Installing default dev.cfg
    Installing default prod.cfg
    Initializing zc.buildout
    Creating directory '/tmp/my-project-name/.duke/bin/'.
    Creating directory '/tmp/my-project-name/.duke/parts/'.
    Creating directory '/tmp/my-project-name/.duke/eggs/'.
    Creating directory '/tmp/my-project-name/.duke/develop-eggs/'.
    Generated script '/tmp/my-project-name/.duke/bin/buildout'.
    Installing dev hooks
    Done!

As you can see, the init command setup and configure `buildout` for the
project and put most of the stuff in a folder name `.duke/`. **This folder
should not be added to your VCS.** It is meant to be recreated easily.

.. caution::
    It's important to understand the difference between `my-project-name`
    and `myprojectname`. The first is only the folder containing your project.
    Its name doesn't really matters. If you are using SVN you should probably
    use trunk as folder name to match SVN folder naming conventions.

    On the other side, `myprojectname` is your real django project name. Duke
    will create it automatically only if there isn't already a project of that
    name in the folder.

Once the initialization done, django duke automatically enters development
mode (which can be done by typing `duke dev` in your project folder). 

You know when you are in development mode when your shell prompt is prefixed
with a project name like this::

    user@host|myprojectname:~/.../trunk/my-project-name$$ ls
    bootstrap.py  buildout.cfg  dev.cfg  prod.cfg  README.rst  setup.py

You can see django duke created different configuration files which will be covered 
later in the documentation. 

Your command line prompt also has been changed. It now includes your project name so 
you always know in which sandbox you are working on. It also indicate if you are in a 
Subversion or Git repository. This is all customizable.

Building your project
=====================

At this point you need to edit `buildout.cfg` to add the requirements you need 
and buildout your project::

    user@host|myprojectname:~/.../trunk/my-project-name$ buildout
    Getting distribution for 'mr.developer'.
    warning: no files found matching 'README.txt'
    Got mr.developer 1.19.
    Getting distribution for 'buildout.dumppickedversions'.
    Got buildout.dumppickedversions 0.5.
    Getting distribution for 'elementtree'.
    zip_safe flag not set; analyzing archive contents...
    Got elementtree 1.2.6-20050316.
    mr.developer: Creating missing sources dir /tmp/my-project-name/src.
    mr.developer: Queued 'djangodukerecipe' for checkout.
    mr.developer: Cloned 'djangodukerecipe' with git.
    Develop: '/tmp/my-project-name/src/djangodukerecipe'
    Develop: '/tmp/my-project-name/.'
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.3.2.
    Getting distribution for 'z3c.recipe.scripts'.
    Got z3c.recipe.scripts 1.0.1.
    Unused options for buildout: 'downloads-directory'.
    Installing _mr.developer.
    Generated script '/tmp/my-project-name/.duke/bin/develop'.
    Installing python.
    Getting distribution for 'simplejson'.
    zip_safe flag not set; analyzing archive contents...
    simplejson.tests.__init__: module references __file__
    Got simplejson 2.3.2.
    Generated interpreter '/tmp/my-project-name/.duke/bin/python'.
    Installing djangodev.
    Generated script '/tmp/my-project-name/.duke/bin/djangodev'.
    Generated script '/tmp/my-project-name/.duke/bin/djangodev.wsgi'.


Once buildout has been run for the first time, you'll see new files in your project
folder::

    user@host|myprojectname|svn:~/.../trunk/my-project-name$ ls -a
    bootstrap.py  buildout.cfg  dev.cfg  .duke  myprojectname/
    my_project_name.egg-info/  prod.cfg  README.rst  setup.py  src/


Start working !
===============

At this point you can start working on your django project::

    user@host|myprojectname|svn:~/.../trunk/my-project-name$ cd projectname/
    user@host|myprojectname|svn:~/.../trunk/my-project-name$ django syncdb
    user@host|myprojectname|svn:~/.../trunk/my-project-name$ django runserver

You don't need to type `python manage.py`, there is a short cut named `django`.
In fact there is many useful shortcuts for django:

* dbshell
* dumpdata
* loaddata
* runserver
* shell
* syncdb

To see the full list of available commands type `duke help`.

Customization
=============

You can tweak your development environment quite alot. 

To do so, simply type this command::

    user@host$ duke customize
    Copying setup.py to ~/.duke/templates/
    Copying profile to ~/.duke/templates/
    Copying bootstrap.py to ~/.duke/templates/
    Copying gitignore to ~/.duke/templates/
    Copying buildout.cfg to ~/.duke/templates/
    Copying project_conf.yml to ~/.duke/templates/
    Copying dev to ~/.duke/templates/
    Copying env to ~/.duke/templates/
    Copying duke_conf.yml to ~/.duke/templates/
    Copying base.cfg to ~/.duke/templates/
    Copying svnignore to ~/.duke/templates/
    Copying dev.cfg to ~/.duke/templates/

Now any modification made to files copied in `~/.duke/templates/` will take 
precedence over those used normally by duke.

If you want to change the command prompt, you will need to modify `~/.duke/templates/profile`.

If there is not enough options for your taste, you can tweak `~/.duke/templates/env`. Be warned 
that it might put your bashfu to test.

Note that you will need to restart your environment for the changes to take effect.

To do so, simply hit Ctrl+D (or exit) and retype `duke dev`.

Finally, resist the temptation of editing files in `.duke/bin/` as they are recreated each 
time you run the buildout command. Per project configuration is not supported as now, but it
should be sufficiently easy to implement to be supported sooner than later.

Don't hesitate to share your improvements with me ! :)

References
----------

+-------------------+--------------------------------------------------------+
| setup.py          | http://www.buildout.org/docs/tutorial.html             |
+-------------------+--------------------------------------------------------+
| Buildout          | http://www.buildout.org/docs/                          |
|                   | http://pypi.python.org/pypi/zc.buildout/1.5.2          | 
+-------------------+--------------------------------------------------------+
| djangorecipe      | http://pypi.python.org/pypi/djangorecipe/0.99          |
+-------------------+--------------------------------------------------------+
| z3c.recipe.scripts| http://pypi.python.org/pypi/z3c.recipe.scripts         |
+-------------------+--------------------------------------------------------+
| mr.developer      | http://pypi.python.org/pypi/mr.developer               |
+-------------------+--------------------------------------------------------+
| Django            | https://docs.djangoproject.com/                        |
+-------------------+--------------------------------------------------------+
| django/buildout   | http://jacobian.org/writing/django-apps-with-buildout/ |
+-------------------+--------------------------------------------------------+