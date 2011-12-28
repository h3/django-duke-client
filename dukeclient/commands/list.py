from dukeclient import client
from dukeclient.commands import BaseCommand


class ListCommand(BaseCommand):

    accept_kwargs = ['servers', 'projects']

    def call(self, *a, **k):
        print client.send(command='list', args=a, flags=k)
