# -*- coding: utf-8 -*-

import os, sys
import dukeclient

from dukeclient.commands import BaseCommand
from dukeclient.utils import create_from_template
from dukeclient.utils.shell import prompt

EMPTY = 1
TEMPLATE = 2
DIR = 3
BINARY = 4

ARCHI = [
    (DIR,"<app-name>",(
        (EMPTY,"__init__.py"),
        (TEMPLATE,"models.py"),
        (TEMPLATE,"tests.py"),
        (TEMPLATE,"urls.py"),
        (TEMPLATE,"views.py"),
        (DIR,"static",(
            (DIR,"<app-name>",(
                (DIR,"css"),
                (DIR,"img",(
                    (BINARY,"motion.png"),#logo
                ),),
                (DIR,"js"),
                (DIR,"sass",(
                    (TEMPLATE,"css3.scss"),
                    (TEMPLATE,"site.scss"),
                ),),
                )
            ),),
        ),
        (DIR,"templates",(
            (TEMPLATE,"base.html"),
            (DIR,"<app-name>",(
                (TEMPLATE,"home.html"),
            ),),
        ),),
        (DIR,"templatetags",(
            (EMPTY,"__init__.py"),
            (TEMPLATE,"<app-name>_tags.py"),
        ),),
    ),),
]






class StartappCommand(BaseCommand):
    """
    Create a new app from scratch.
    """

    options   = [
        ('-b', '--base-path', {
            'dest': 'base_path', 
            'help': 'Directory where the app should be created.'}),
    ]

    def call(self, *args, **options):
        self._options = options
        self.base_path = 'base_path' in options and options['base_path'] or os.getcwd()

        if len(args) < 1:
            self.error("usage: duke startapp <app-name> [options]\n")

        if os.environ.get('DUKE_ENV') is not None:
            self.error("you cannot start a duke project from within a duke instance.\n")

        project_name = args[0].replace('/', '')
        project_path = os.path.join(self.base_path, project_name)

        if os.path.exists(project_path):
            self.error("Could not create project \"%s\", directory already exists." % project_name)

        def make(x,path):
            if x[0] == EMPTY:
                self.local('touch %s' % os.path.join(path, x[1].replace('<app-name>',project_name)))
            elif x[0] == TEMPLATE:
                create_from_template(os.path.join('startapp',x[1]), path, variables={
                    'project_name': project_name,
                    'duke_client_version': dukeclient.VERSION,
                },dest_name=x[1].replace("<app-name>",project_name))
            elif x[0] == DIR:
                os.makedirs(os.path.join(path,x[1].replace("<app-name>",project_name)))
            elif x[0] == BINARY:
                create_from_template(os.path.join('startapp',x[1]), path,dest_name=x[1].replace("<app-name>",project_name))
                pass


        def loop(x,path=""):
            if len(x) >= 2:
                make(x,path)
            if len(x) >= 3 and x[0] == DIR:
                for u in x[2]:
                    if path :
                        loop(u,os.path.join(path,x[1].replace("<app-name>",project_name)))
                    else:
                        loop(u,x[1].replace("<app-name>",project_name))
        
        for u in ARCHI:
            loop(u,self.base_path)

        self.info("Created app %s" % project_name)
