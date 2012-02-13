import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
from dukeclient.utils.shell import prompt


class StartprojectCommand(BaseCommand):
    """
    Create a new project from scratch.
    """

    options   = []
    base_path = os.getcwd()

    def call(self, *args, **options):
        if len(args) < 2:
            self.error("usage: duke startproject <project-name> [options]\n")

        project_name = args[1].replace('/', '')
        project_path = os.path.join(self.base_path, project_name)

        if os.path.exists(project_path):
            self.error("Could not create project \"%s\", directory already exists." % project_name)
        
        os.makedirs(project_path)

        create_from_template('setup.py', project_path, {
            'project_name': project_name,
            'duke_client_version': dukeclient.VERSION,
        })
        
        self.local('touch %s' % os.path.join(project_path, 'README.rst'))
       #self.local('touch %s' % os.path.join(project_path, 'LICENSE'))
       #self.local('touch %s' % os.path.join(project_path, 'CHANGELOG'))

       #django_project_name = prompt('Django project name:', validate=r'^[_a-zA-Z]\w*$', 
       #        default=project_name.split('.')[0].replace('-','_'))

        self.info("Created project %s" % project_name)
