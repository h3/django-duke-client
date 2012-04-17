============
Deploying
============

.. contents::
   :depth: 3

Warning
=======




With fabric
===========

.. caution::

   This is pretty much alpha stuff, it might change a lot in the future.

Currently the duke client only offer some useful `fabric`_ tasks for 
standard django deployment.

Configuration
-------------

To use it, simply create a file named `fabfile.py` in the root directory of 
your project (where your `setup.py` file is).

The file content should look like this::

    import os

    from dukeclient.fabric.utils import get_role, get_conf, get_project_path
    from dukeclient.fabric.tasks import *

    LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

    env.roledefs.update({
        'demo': ['user@demo.host.com'],
        'prod': ['user@production.host.com:5555'],

        # Not required, but can be useful if you want to invoke commands 
        # on multiple servers at once.
        'http_servers': ['user@production.host.com:5555', 'user@demo.host.com'],
    })

    env.site = {
        'domain':   'mysite.com',
        'package':  'mysite.com',
        'project':  'mysite',
        'repos':    'svn://svn.myserver.com/mysite.com/trunk/mysite.com/',
    }

    env.roleconfs = {
        
        # This is an example of how you can deploy on Plesk
        'prod': {
            'hosts': env.roledefs['prod'],
            'user': 'username',
            'group': 'usergroup',
            'document-root': '/var/www/vhosts/%(domain)s/httpdocs/',
            'vhost-conf': '/var/www/vhosts/%(domain)s/conf/vhost.conf',

            # Most commands uses an event system which will run scripts
            # at specific times.
            'on-code-sync': [],
            'on-code-sync-done': [],
            'on-apache-reload': [
                # You can run scripts before and after most of the available 
                # commands. In this case we tell Plesk to reload its vhost 
                # configuration for mysite.com
                '/usr/local/psa/admin/sbin/websrvmng --reconfigure-vhost --vhost-name=%(domain)s',
            ],
            'on-apache-reload-done': [],

            # If mod_python is installed on your Apache server, you'll need 
            # virtualenv or you will go insane. Really.
            'virtualenv': True,
        },

        # This example show a more basic Apache deployment
        'demo': {
            'hosts': env.roledefs['demo'],
            'document-root': '/var/www/vhosts/demo.%(domain)s/',
            'media-root':  '/var/www/vhosts/demo.%(domain)s/%(domain)s/%(project)s/media/',
            'static-root': '/var/www/vhosts/demo.%(domain)s/%(domain)s/static/',
            'vhost-conf': '/etc/apache2/sites-enabled/demo.%(domain)s',
            'virtualenv': True,
            'user': 'www-data',
            'group': 'www-data',
            'on-deploy-done': [
                'ln -sf /var/www/vhosts/demo.%(domain)s/%(domain)s/%(project)s/media/ /var/www/vhosts/demo.%(domain)s/media',
            ],
        },

    }


Usage
-----

Deploying
^^^^^^^^^

On `demo`::

    fab -R demo full_deploy

On `prod`::

    fab -R prod full_deploy

On both::

    fab -R http_servers full_deploy

Updating
^^^^^^^^

::

    fab -R prod deploy


.. _`fabric`: http://fabfile.org/

.. caution::

    The `deploy` command will not update externals

Other commands
^^^^^^^^^^^^^^

Other commands will eventually be documented properly .. meanwhile you can 
list them all using the `fab -l` command.


