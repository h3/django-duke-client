import os
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.commands.dev import DevCommand


class InitCommand(BaseCommand):
    """
    Initialize duke for an existing project.
    """

    bootstrap_opts = ' -v 1.7.1'

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
            'help': 'Python version to use (defaults\
 to system default). Ex: python2.7'}),
        ('-q', '--quiet', {
            'action': 'store_true',
            'dest': 'quiet', 'default': False,
            'help': 'No output'}),
    ]

    def setup_paths(self):
        self.duke_path = os.path.join(self.base_path, '.duke/')
        self.eggs_path = os.path.join(self.duke_path, 'cache/eggs/')
        self.download_path = os.path.join(self.duke_path, 'cache/download/')
        self.bin_path = os.path.join(self.duke_path, 'bin/')
        self.conf_path = os.path.join(os.getenv("HOME"), '.duke/')

        # create directories if needed
        for path in ['base', 'duke', 'eggs', 'download', 'bin', 'conf']:
            p = getattr(self, '%s_path' % path, None)
            if p and not os.path.exists(p):
                os.makedirs(p)

    def get_context(self):
        # Variables passed to generated .cfg files
        return {
            'duke_client_version': dukeclient.VERSION,
            'project_name': self.project_name,
            'parent_dirname': self.parent_dir,
            'base_path': self.base_path,
            'duke_path': self.duke_path,
            'eggs_path': self.eggs_path,
            'download_path': self.download_path,
            'settings_module': 'settings',
        }

    def install_files(self):
        self.install_file('bootstrap.py', self.base_path)
        self.install_file('buildout.cfg', self.base_path, self.context)
        self.install_file('base.cfg', self.duke_path, self.context)
        self.install_file('dev.cfg', self.base_path, self.context)

    def install_dev_hooks(self):
        # Dev source
        if not self.call_opts['quiet']:
            self.info("Installing dev hooks")

        self.install_file('dev', self.bin_path, self.context)
        self.install_file('env', self.bin_path, self.context)
        self.install_file('profile', self.bin_path, self.context)

    def install_project_confs(self):
        # The project_conf.yml might have local modifications so we want
        # to preserve it.
        conf_path = os.path.join(self.duke_path, 'project_conf.yml')
        if not os.path.exists(conf_path):
            self.install_file('project_conf.yml', self.duke_path, self.context)

    def initialize_buildout(self):
        if not self.call_opts['quiet']:
            self.info("Initializing zc.buildout")

        # Even though distribute is considered superior and better maintained
        # than setuptools, it is disabled by default because I cannot get the
        # project sandboxing to work properly with it .. bummer.
        if self.call_opts['distribute']:
            if not self.call_opts['quiet']:
                self.info("Using distribute")
            self.bootstrap_opts = ' '.join([self.bootstrap_opts, '-d'])

        # Temporarely forcing bootstrap 1.7.1
        # since 2.0 seems to breaks everything it can break
        python = self.call_opts['python'] or 'python'  # and python !

        command = '%s bootstrap.py%s' % (python, self.bootstrap_opts)
        status, output = self.local(command)

        if not self.call_opts['quiet']:
            self.debug(output)

    def call(self, *args, **options):
        self.call_opts = options
        if len(args) < 1:
            self.error("usage: duke init <project> [options]\n")

        # FIXME: Validate for proper python module name
        self.project_name = args[0].replace('/', '').replace('-', '_')
        self.base_path = 'base_path' in options and options['base_path']\
            or os.getcwd()
        self.parent_dir = os.path.basename(os.path.abspath(self.base_path))

        self.setup_paths()
        self.context = self.get_context()

        self.install_files()
        self.initialize_buildout()
        self.install_dev_hooks()
        self.install_project_confs()

        if not self.call_opts['quiet']:
            self.info("\nDone! Now type \"buildout\"\
to build the environment and install requirements.\n")

        if not options['nodev']:
            DevCommand().call()
