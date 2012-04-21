============
Deploying
============

.. contents::
   :depth: 3


With fabric
===========

.. caution::

   This is pretty much alpha stuff, it might change a lot in the future.

Currently the duke client only offer some useful `fabric`_ tasks for 
standard django deployment.

Project Configurations
----------------------

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

Deployment configurations
-------------------------

Deployment configurations must be stored in a directory named `deploy/` in
the root directory of your project.


Virtualhost
^^^^^^^^^^^

Virtual host files a threated as template, so you don't have to adjust them 
every time you change a configuration.

The naming convention is `<role>.vhost`. So if you have a `demo` and a `prod`
role, your vhost files should be name `demo.vhost` and `prod.vhost`.

Here's an example of a standard Apache/WSGI vhost configuration file::

    <VirtualHost *:80>
        ServerAdmin max@motion-m.ca
        DocumentRoot %(document-root)s
        ServerName %(project)s.d.motion-m.ca
        ErrorLog /var/log/apache2/%(package)s.d.motion-m.ca-error_log
        CustomLog %(project)s.d.motion-m.ca common
        Options FollowSymLinks
        WSGIPassAuthorization On
        WSGIScriptAlias / %(document-root)s%(package)s/%(project)s/wsgi.py
        WSGIDaemonProcess %(project)s user=www-data group=www-data processes=5 threads=1
        WSGIProcessGroup %(project)s
        Alias /static/ %(document-root)sstatic/
        Alias /media/ %(document-root)smedia/
        <Directory %(document-root)smedia/>
            Order deny,allow
            Allow from all
            AllowOverride None
        </Directory>
        <Directory %(document-root)sstatic/>
            Order deny,allow
            Allow from all
            AllowOverride None
        </Directory>
    </VirtualHost>


Settings.py
^^^^^^^^^^^

The settings.py files can be automatically overwritten with a settings.py template.

For example, to set your project's settings on a role named `demo` you would start
by creating a file named `deploy/demo_settings.py`.

Now every time you deploy your code, the file `deploy/demo_settings.py` gets copied 
over `myproject/local_settings.py`, overriding any other settings set elsewhere.

Here's an example which defines the default database backend::

    from %(project)s.conf.settings.default import *

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%(project)s_demo',
            'USER': '%(project)s',
            'PASSWORD': '*********',
        }
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

Per role configurations
^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you want to tweak configurations depending on which role the project
is running on.

To accomplish this, simply create a `cfg` file named after the role and make it 
extend the `buildout.cfg` file. 

The next time buildout will be run on this role, it will find the file and use it
instead of `buildout.cfg`.

Here's an example of how one could set a cron job on the production server:

**prod.cfg**::

    [buildout]
    extends = buildout.cfg
    parts += django-cleanup
    
    [django-cleanup]
    recipe = z3c.recipe.usercrontab
    times = @monthly
    command = ${buildout:directory}/.duke/bin/django cleanup


Development roadmap
===================

In the long term a `django duke master` will be created. The scope of the
functionalities isn't yet fixed, but it's main purpose will be to act as a
deployment server. It will hold servers and projects configurations and allow
easy deployment using the `duke` command.

There is several advantages of using centralized deployment  instead 
of a distributed deployment strategy (with fabric). But the most important 
advantage for us is to be able to assign deployment rights to developers without
giving them actual access to the production servers.

When centralized deployment will be implemented, we will probably move to other
nice to have features like scheduled deployment and continous integration.