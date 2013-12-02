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
        ('-b', '--base-path', {
            'dest': 'base_path',
            'help': 'Directory where the project should be created.'}),
    ]

    def call(self, *args, **options):
        self._options = options
        self.base_path = 'base_path' in options and options['base_path'] or os.getcwd()

        if len(args) < 1:
            self.error("usage: duke startproject <project-name> [options]\n")

        if os.environ.get('DUKE_ENV') is not None:
            self.error("you cannot start a duke project from within a duke instance.\n")
       #else:
       #    django_project_name = prompt('Django project name:', validate=r'^[_a-zA-Z]\w*$',
       #            default=project_name.split('.')[0].replace('-','_'))

        project_name = args[0].replace('/', '')

        if len(args) > 1 and args[1] == '.':
            project_path = self.base_path
        else:
            project_path = os.path.join(self.base_path, project_name)

            if os.path.exists(project_path):
                self.error("Could not create project \"%s\", directory already exists." % project_name)
            else:
                os.makedirs(project_path)

        create_from_template('setup.py', project_path, {
            'project_name': project_name,
            'duke_client_version': dukeclient.VERSION,
        })

        self.info("Created project %s" % project_name)
