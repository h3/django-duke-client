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

Installation
------------

We're not even in pre-alpha so the only way to install it right now is from 
source::

   $: git clone git://github.com/h3/django-duke-client.git
   $: cd django-duke-client/
   $: sudo python setup.py develop

Minimal project layout
----------------------

The django duke client tries to be independent as possible
in term of project layout. However a minimal structure is
required for it to work properly.

This is the minimal project layout to initialize duke::

    project-root-folder/
      - setup.py
      + src/
      + projectname/ *
        - settings.py
        - development.py
        - production.py

* The django project is actually optionnal, if it isn't present it will be 
  created automatically when running buildout. Note that if you start from
  an existing project you should still create the development.py and 
  production.py settings files.

When the project is built, it looks like this::

    project-root-folder/
      - bootstrap.py
      - buildout.cfg
      - dev.cfg
      - setup.py
      + bin/
      + develop-eggs/
      + project_root_folder.egg-info
      + eggs/
      + parts/
      + src/
      + projectname/
        - settings.py
        - development.py
        - production.py

Most of the directory and files created by duke should not be added to your 
VCS. This way you can trash and reload the entire environment easily using
`duke clean` and `duke init <projectname>`.

This is what the above project would look like after running the `duke clean`
command::

    project-root-folder/
      - buildout.cfg
      - dev.cfg
      - setup.py
      + projectname/
        - settings.py
        - development.py
        - production.py

What's left is basically what should be in your VCS.

Commands
--------

Duke
^^^^

All duke client commands are invoked using `duke` like such::

    $: duke <command>

Here's the list of available duke commands so far:

 +--------------+----------------+-----------------------------------+
 | Command      | Args           | Description                       | 
 +--------------+----------------+-----------------------------------+
 | clean        |                | Cleanup dev environment           |
 +--------------+----------------+-----------------------------------+
 | dev          |                | Activate development mode         |
 +--------------+----------------+-----------------------------------+
 | init         | <project>      | Initialize duke on a project      |
 +--------------+----------------+-----------------------------------+
 | startproject | <project-root> | Initialize a project from scratch |
 +--------------+----------------+-----------------------------------+

Dev
^^^

When the development environment has been activated some shell commands become
available (no need to type duke before).

 +------------+------------------------------------------+
 | Command    | Description                              | 
 +------------+------------------------------------------+
 | buildout   | Run buildout                             |
 +------------+------------------------------------------+
 | deactivate | Deactivates the development environment. |
 +------------+------------------------------------------+
 | django     | Use this instead of manage.py            |
 +------------+------------------------------------------+
 | python     | A sandboxed python interpreter           |
 +------------+------------------------------------------+
 | run_tests  | Runs the django test suite *             |
 +------------+------------------------------------------+

 * If you look in the `./bin/` directory you'll notice that the script isn't
   named "run_tests" but "test". While there is no problem running the test
   from the relative path (ex: `./bin/test`), making `test` available globally 
   breaks things because of a clash with `/usr/bin/test`.

All these commands are scripts that reside in `./bin/`. The development 
environment makes them available globally.

Of course there can be more depending on your buildout configuration.

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
    README.rst  setup.py

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

    $: duke dev
    $(duke-website): buildout
    Develop: '~/www/duke-website/.'
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.3.2.
    Uninstalling python.
    Installing python.
    Generated interpreter '~/www/duke-website/bin/python'.

In dev mode, duke does some magic behind the scene to make your life easier.
This is why I don't need to run ./bin/buildout and instead I can just run 
buildout which will in fact run ./bin/buildout -c dev.cfg when working in dev 
mode. 

Duke makes the binaries and script living int ./bin/ available 
locally. Once you get out of dev mode, these command shortcuts wont be 
available anymore.. until you re-enter the dev mode of course.

You'll also notice that buildout installs a python binary in ./bin/. This 
means that when you invoke the python interpreter in dev mode, it actually 
invoke ./bin/python which is a sandboxed python. This allows encapsulation 
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

