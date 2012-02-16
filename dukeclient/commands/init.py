import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.commands.dev import DevCommand
from dukeclient.utils import create_from_template

class InitCommand(BaseCommand):
    """
    Initialize duke for an existing project.
    """

    options = [
        ('-d', '--distribute', {
            'dest': 'distribute', 'action': 'store_true', 'default': False,
            'help': 'Use distribute instead of setuptools'}),
        ('-p', '--python', {
            'dest': 'python', 
            'help': 'Python version to use (defaults to system default). Ex: python2.7'}),
    ]

    def call(self, *args, **options):
        self.base_path = os.getcwd()
        self.duke_path = os.path.join(self.base_path, '.duke/')
        self.bin_path  = os.path.join(self.duke_path, 'bin/')

        if len(args) < 2:
            self.info("usage: duke init <project> [options]\n")
            sys.exit(1)

        if not os.path.exists(self.duke_path):
            os.makedirs(self.duke_path)

        project_name = args[1].replace('/', '')

        # bootstrap.py
        if os.path.exists(os.path.join(self.base_path, 'bootstrap.py')):
            self.warning("Found a bootstrap.py file.. skipping its creation.")
        else:
            self.info("Installing bootstrap.py..")
            create_from_template('bootstrap.py', self.base_path)

        # Variables passed to generated .cfg files
        context = {
            'duke_client_version': dukeclient.VERSION,
            'project_name': project_name,
            'parent_dirname': os.path.basename(os.path.abspath(self.base_path)),
            'base_path': self.base_path,
            'duke_path': self.duke_path,
            # FIXME: todo, find out the settings file name from the dev.cfg file in the [djangodev] section
            # http://svn.zope.org/zc.buildout/trunk/src/zc/buildout/buildout.py?rev=123007&view=markup
            # see the_read_installed_part_options method for parsing example
            'settings_module': 'settings_dev',
        }

        # buildout.cfg
        if os.path.exists(os.path.join(self.base_path, 'buildout.cfg')):
            self.info("A buildout.cfg has been found, will be using it.")
        else:
            self.info("Installing default buildout.cfg")
            create_from_template('buildout.cfg', self.base_path, context)

        # .duke/base.cfg
        if os.path.exists(os.path.join(self.duke_path, 'base.cfg')):
            self.info("A base.cfg has been found, will be using it.")
        else:
            self.info("Installing default base.cfg")
            create_from_template('base.cfg', self.duke_path, context)

        # .duke/dev.cfg
        if os.path.exists(os.path.join(self.base_path, 'dev.cfg')):
            self.info("A dev.cfg has been found, will be using it.")
        else:
            self.info("Installing default dev.cfg")
            create_from_template('dev.cfg', self.base_path, context)

        # .duke/prod.cfg
        if os.path.exists(os.path.join(self.base_path, 'prod.cfg')):
            self.info("A prod.cfg has been found, will be using it.")
        else:
            self.info("Installing default prod.cfg")
            create_from_template('prod.cfg', self.base_path, context)

        self.info("Initializing zc.buildout")
        
        boot_opts = ''
        python = options['python'] or 'python' # and python !

        # Even though distribute is considered superior and better maintained
        # than setuptools, it is disabled by default because I cannot get the
        # project sandboxing to work properly with it .. bummer.
        if options['distribute']:
            opts = ' -d'

        status, output = self.local('%s bootstrap.py%s' % (python, boot_opts))
        self.debug(output)

        # Dev source
        self.info("Installing dev hooks")

        if not os.path.exists(self.bin_path):
            os.makedirs(self.bin_path)

        create_from_template('dev', self.bin_path, context)
        create_from_template('env', self.bin_path, context)

        self.info("Done! (It is recommanded to add only bootstrap.py, buildout.cfg and dev.cfg to your VCS).\n")
        self.info("Edit buildout.cfg and dev.cfg to configure and type \"buildout\" to install requirements.")

        DevCommand().call()
