import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils.conf import ProjectConfigManager
import dukeclient


class DevCommand(BaseCommand):

   #options = [
   #    ('-p', '--python', {'dest': 'python'}),
   #]


    def call(self, *args, **options):
        self.base_path = os.getcwd()
        if not os.path.exists(os.path.join(self.base_path, '.duke/')):
            if os.path.exists(os.path.join(self.base_path, 'setup.py')):
                self.error("not within a duke managed project, but a setup.py \
file has been found. Initialize this project with this command\n\
$ duke init <project_name>")
            else:
                self.error("not within a duke managed project.")

        self.project = ProjectConfigManager(self.base_path)
        self.duke_path = os.path.join(self.base_path, '.duke/')
        self.bin_path  = os.path.join(self.duke_path, 'bin/')

        if os.getenv("DUKE_ENV"):
            env = os.path.basename(os.getenv("DUKE_ENV"))
            self.error("dev environment \"%s\" already loaded" % env)
        else:
            context = {
                'duke_client_version': dukeclient.VERSION,
                'project_name': self.project.get('name'),
                'parent_dirname': os.path.basename(os.path.abspath(self.base_path)),
                'base_path': self.base_path,
                'duke_path': self.duke_path,
                'settings_module': 'settings',
            }

            self.install_file('dev', self.bin_path, context, quiet=True, overwrite=True)
            self.install_file('env', self.bin_path, context, quiet=True, overwrite=True)
            self.install_file('profile', self.bin_path, context, quiet=True, overwrite=True)

            devsrc = os.path.join(context.get('duke_path'), 'bin/dev')
            dukerc = os.path.join(context.get('base_path'), '.dukerc')
            
            if os.path.exists(dukerc):
                os.system('bash --rcfile %s' % dukerc)
            else:
                os.system('bash --rcfile %s' % devsrc)
