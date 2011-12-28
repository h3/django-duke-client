from dukeclient import client
from dukeclient.commands import BaseCommand


class ListCommand(BaseCommand):

    def call(self, *a, **k):
        client.send(command='list', args=a, flags=k)
