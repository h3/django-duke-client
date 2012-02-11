django-duke-client
==================

Commands
--------

All client commands are invoked using `duke` like such::

    $: duke clean

Here's the list of available commands so far:

 +----------+-----------+------------------------------+
 | Command  | Args      | Description                  | 
 +----------+-----------+------------------------------+
 | clean    |           | Cleanup dev environment      |
 +----------+-----------+------------------------------+
 | dev      |           | Activate development mode    |
 +----------+-----------+------------------------------+
 | init     | <project> | Initialize duke on a project |
 +----------+-----------+------------------------------+


Workflow
--------

Here's a real world example of how you can use duke to bootstrap a project, please note
that duke commands must be run within the root folder of you project::

    $: cd ~/www/
    $: git clone git://github.com/h3/duke-website.git
    $: cd duke-website/
    $: ls
    README.rst  setup.py  website

The a setup.py file and a python module is the bare minimum required to get started.
You can see what the setup.py file looks like (and use it as template) at this URL:
https://github.com/h3/duke-website/blob/master/setup.py

Now we want to bootstrap the project, which basically means setup buildout for it::

    $: duke init src/website/
    Initializing zc.buildout
    Debug: Downloading http://pypi.python.org/packages/source/d/distribute/distribute-0.6.24.tar.gz
    Extracting in /tmp/tmpMsayuc
    Now working in /tmp/tmpMsayuc/distribute-0.6.24
    Building a Distribute egg in /tmp/tmpL3w1Wn
    /tmp/tmpL3w1Wn/distribute-0.6.24-py2.7.egg
    Creating directory '~/www/duke-website/bin'.
    Creating directory '~/www/duke-website/parts'.
    Creating directory '~/www/duke-website/eggs'.
    Creating directory '~/www/duke-website/develop-eggs'.
    Generated script '~/www/duke-website/bin/buildout'.
    Installing dev hooks
    Done. It is recommanded to add bootstrap.py and buildout.cfg to your VCS.

    $: ls
    bin  bootstrap.py  buildout.cfg  develop-eggs  eggs  parts  README.rst	setup.py  website

As you can see, duke created the bootstrap.py and buildout.cfg files and initialized buildout for you.
The next step is to configure buildout.cfg to meet your requirements and then enter in development mode
to run buildout::

    $: duke dev
    $(duke-website): buildout
    Develop: '~/www/duke-website/.'
    Getting distribution for 'zc.recipe.egg'.
    Got zc.recipe.egg 1.3.2.
    Uninstalling python.
    Installing python.
    Generated interpreter '~/www/duke-website/bin/python'.

En dev mode, duke does some magic behind the scene to make your life easier. This is why I don't need
to run ./bin/buildout and instead I can just run buildout. Duke makes the binaries and script living
int ./bin/ available locally. Once you get out of dev mode, these command shortcuts wont be available
anymore.. until you re-enter the dev mode of course.

You'll notice that buildout installs a python binary in ./bin/. This means that when you invoke the
python interpreter in dev mode, it actually invoke ./bin/python which is a sandboxed python. This 
allows encapsulation of your environment, the modules you install are installed only within 
this environment.

When working in dev mode the project name will be prefixed to your command prompt to indicate in which
project you are working. To leave dev mode simply type `deactivate`.


References
----------

 setup.py               http://www.buildout.org/docs/tutorial.html
 Buildout               http://www.buildout.org/docs/   
                        http://pypi.python.org/pypi/zc.buildout/1.5.2
 djangorecipe           http://pypi.python.org/pypi/djangorecipe/0.99
 z3c.recipe.scripts     http://pypi.python.org/pypi/z3c.recipe.scripts
 mr.developer           http://pypi.python.org/pypi/mr.developer
 Django                 https://docs.djangoproject.com/
 Django + buildout      http://jacobian.org/writing/django-apps-with-buildout/

