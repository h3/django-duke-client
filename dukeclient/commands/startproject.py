import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
from dukeclient.utils.shell import prompt


class StartprojectCommand(BaseCommand):
    """
    Create a new project from scratch.
    """

    options   = [
        ('-m', '--minimal', {
            'dest': 'minimal', 
            'help': 'Create only the project folder with the setup.py file (no readme/license/tests.'}),
        ('-b', '--base-path', {
            'dest': 'base_path', 
            'help': 'Directory where the project should be created.'}),
    ]

    def call(self, *args, **options):
        self.base_path = options.get('base_path', os.getcwd())

        if len(args) < 2:
            self.error("usage: duke startproject <project-name> [options]\n")
       #else:
       #    django_project_name = prompt('Django project name:', validate=r'^[_a-zA-Z]\w*$', 
       #            default=project_name.split('.')[0].replace('-','_'))

        project_name = args[1].replace('/', '')
        project_path = os.path.join(self.base_path, project_name)

        if os.path.exists(project_path):
            self.error("Could not create project \"%s\", directory already exists." % project_name)
        
        os.makedirs(project_path)

        create_from_template('setup.py', project_path, {
            'project_name': project_name,
            'duke_client_version': dukeclient.VERSION,
        })

        if not options['minimal']:
            os.makedirs(os.path.join(project_path, 'tests/'))
            self.local('touch %s' % os.path.join(project_path, 'README.rst'))
            self.local('touch %s' % os.path.join(project_path, 'LICENSE'))

        self.info("Created project %s" % project_name)
