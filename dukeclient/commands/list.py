from dukeclient import client
from dukeclient.commands import BaseCommand


class ListCommand(BaseCommand):

    options = [
        ('-m', '--master', {'metavar': 'SERVER', 'dest': 'server'}),
    ]

    def call(self, *a, **k):
        print client.send(command='list', args=a, flags=k)
