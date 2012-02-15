============
Installation
============

.. contents::
   :depth: 3

Official releases
=================

Official releases will eventually be available from `PyPI`_.

Download the .zip distribution file and unpack it. Inside is a script
named ``setup.py``. Enter this command::

   python setup.py install

...and the package will install automatically.

.. _`PyPI`: http://pypi.python.org/pypi/django-duke-client/


Development version
===================

Alternatively, you can get the latest source from our `git`_ repository::

   git clone git://github.com/h3/django-duke-client.git

Add the resulting folder to your `PYTHONPATH`_ or symlink the ``dukeclient`` 
directory inside it into a directory which is on your PYTHONPATH, such as 
your Python installation's ``site-packages`` directory.

You can verify that the application is installed by typing the following
command in a terminal::

   $: duke help


When you want to update your copy of the source code, run ``git pull``
from within the ``django-duke-client`` directory.

.. caution::

   The development version may contain bugs which are not present in the
   release version and introduce backwards-incompatible changes.

   If you're tracking master, keep an eye on the recent `Commit History`_ 
   before you update your copy of the source code.

.. _`git`: http://git-scm.com/
.. _`PYTHONPATH`: http://docs.python.org/tut/node8.html#SECTION008110000000000000000
.. _`Commit History`: https://github.com/h3/django-duke-client/commits/master
