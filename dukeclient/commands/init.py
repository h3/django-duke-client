import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.commands.dev import DevCommand

class InitCommand(BaseCommand):
    """
    Initialize duke for an existing project.
    """

    options = [
        ('-b', '--base-path', {
            'dest': 'base_path', 
            'help': 'Directory where the project should be initialized.'}),
        ('-d', '--distribute', {
            'dest': 'distribute', 'action': 'store_true', 'default': False,
            'help': 'Use distribute instead of setuptools'}),
        ('-n', '--nodev', {
            'dest': 'nodev', 'action': 'store_true', 'default': False,
            'help': 'Do not launch development env once init is complete'}),
        ('-p', '--python', {
            'dest': 'python', 
            'help': 'Python version to use (defaults to system default). Ex: python2.7'}),
    ]

    def call(self, *args, **options):
        if len(args) < 1:
            self.error("usage: duke init <project> [options]\n")

        # FIXME: Validate for proper python module name
        project_name = args[0].replace('/', '').replace('-', '_')

        self.base_path = 'base_path' in options and options['base_path'] or os.getcwd()
        self.duke_path = os.path.join(self.base_path, '.duke/')
        self.bin_path  = os.path.join(self.duke_path, 'bin/')
        self.conf_path = os.path.join(os.getenv("HOME"), '.duke/')

        if not os.path.exists(self.duke_path):
            os.makedirs(self.duke_path)

        if not os.path.exists(self.conf_path):
            os.mkdir(self.conf_path)

        # Variables passed to generated .cfg files
        context = {
            'duke_client_version': dukeclient.VERSION,
            'project_name': project_name,
            'parent_dirname': os.path.basename(os.path.abspath(self.base_path)),
            'base_path': self.base_path,
            'duke_path': self.duke_path,
            'settings_module': 'settings',
        }

        if not os.path.exists(os.path.join(self.conf_path, 'duke_conf.yml')):
            self.info("Creating default global configuration file")
            self.install_file('duke_conf.yml', self.conf_path, context)

        self.install_file('bootstrap.py', self.base_path)
        self.install_file('buildout.cfg', self.base_path, context)
        self.install_file('base.cfg', self.duke_path, context)
        self.install_file('dev.cfg', self.base_path, context)

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

        self.install_file('dev', self.bin_path, context)
        self.install_file('env', self.bin_path, context)
        self.install_file('profile', self.bin_path, context)

        # The project_conf.yml might have local modifications so we want
        # to preserve it.
        if not os.path.exists(os.path.join(self.duke_path, 'project_conf.yml')):
            self.install_file('project_conf.yml', self.duke_path, context)

        self.info("Done!\n")
        self.info("Type \"buildout\" to build the environment and install requirements.")

        if not options['nodev']:
            DevCommand().call()
