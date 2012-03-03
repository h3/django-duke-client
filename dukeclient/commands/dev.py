import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils.conf import ProjectConfigManager
import dukeclient


class DevCommand(BaseCommand):

   #options = [
   #    ('-p', '--python', {'dest': 'python'}),
   #]

    base_path = os.getcwd()
    project = ProjectConfigManager(base_path)

    def call(self, *args, **options):
        if not os.path.exists(os.path.join(self.base_path, '.duke/')):
            self.error("not within a duke managed project.")

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
            self.install_file('dev', self.bin_path, context, quiet=True)
            self.install_file('env', self.bin_path, context, quiet=True)
            self.install_file('profile', self.bin_path, context, quiet=True)

            os.system('bash --rcfile .duke/bin/dev')
