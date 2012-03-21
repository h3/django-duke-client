django-duke-client
==================

Django duke client aims provide a turnkey development environment for django 
and make django development easier and faster.

It is currently built for the new project layout of django 1.4. The older 
project layout support might be implemented someday, but right now it's not
a priority.

It makes heavy uses of buildout. My first attempt was using pip+virtualenv,
but it soon became evident that buildout was the way to go in term of 
efficiency and extensibility.

Official documentation: http://readthedocs.org/docs/django-duke-client/en/latest/

Installation
------------

We're not even in pre-alpha so the only way to install it right now is from 
source::

   $: git clone git://github.com/h3/django-duke-client.git
   $: cd django-duke-client/
   $: sudo python setup.py develop

For the impatients
------------------

Create a project::

    duke startproject test-project
    cd test-project
    duke init testproject
    buildout

Minimal project layout
----------------------

The django duke client tries to be independent as possible
in term of project layout. However a minimal structure is
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


Note: `.duke/` should not be added to your VCS nor you should modify files in it by hand. It is meant to be rebuild easily.

Workflow
--------

Here's a real world example of how you can use duke to bootstrap a project, 
please note that duke commands must be run within the root folder of you 
project.

Starting from scratch::

    $: duke startproject duke-website
    Created project duke-website
    $: cd duke-website/
    $duke-website/: ls
    README.rst  setup.py tests

Using an exising project::

    $: cd ~/www/
    $: git clone git://github.com/h3/duke-website.git
    $: cd duke-website/
    $: ls
    README.rst  setup.py  dukewebsite

The a setup.py file and a python module is the bare minimum required to get 
started. You can see what the setup.py file looks like (and use it as 
template) at this URL:
https://github.com/h3/duke-website/blob/master/setup.py

Now we want to bootstrap the project, which basically means setup buildout 
for it. Considering our django project is called `dukewebsite`::

    $: duke init dukewebsite
    Installing dev hooks
    Done. It is recommanded to add bootstrap.py and buildout.cfg to your VCS.

    $: ls
    bin  bootstrap.py  buildout.cfg  develop-eggs  eggs  parts  README.rst	
    setup.py  dukewebsite

As you can see, duke created the bootstrap.py and buildout.cfg files and 
initialized buildout for you. The next step is to configure buildout.cfg to 
meet your requirements and then enter in development mode to run buildout::

    user@host$ duke dev
    user@host|dukewebsite|svn:~/.../duke-website/$ buildout
    Develop: '~/www/duke-website/.'
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.3.2.
    Uninstalling python.
    Installing python.
    Generated interpreter '~/www/duke-website/.duke/bin/python'.

In dev mode, duke does some magic behind the scene to make your life easier.
This is why I don't need to run .duke/bin/buildout and instead I can just run 
buildout which will in fact run .duke/bin/buildout -c dev.cfg when working in dev 
mode. 

Duke makes the binaries and script living int .duke/bin/ available 
locally. Once you get out of dev mode, these command shortcuts wont be 
available anymore.. until you re-enter the dev mode of course.

You'll also notice that buildout installs a python binary in .duke/bin/. This 
means that when you invoke the python interpreter in dev mode, it actually 
invoke .duke/bin/python which is a sandboxed python. This allows encapsulation 
of your environment, the modules you install are installed only within this 
environment.

When working in dev mode the project name will be prefixed to your command 
prompt to indicate in which project you are working. To leave dev mode simply 
type `deactivate`.

Bonus
-----

Here's a one liner example to start and initialize a project from scratch::

    duke startproject duke-website && cd duke-website && duke init dukewebsite

Then you only have to edit buildout.cfg (and/or dev.cfg) and type `buildout` to
update dependencies.

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

Credits
=======

This project was created and is sponsored by:

.. figure:: http://motion-m.ca/media/img/logo.png
    :figwidth: image

Motion Média (http://motion-m.ca)