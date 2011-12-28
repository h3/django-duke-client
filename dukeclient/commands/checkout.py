import git

from dukeclient import client
from dukeclient.commands import BaseCommand

class CheckoutCommand(BaseCommand):
    """
    Checkout a project
    """

    accept_kwargs = ['servers', 'projects']

    def call(self, *a, **k):
        rs = self.json(client.send(command='checkout', args=a, flags=k))
        if rs['protocol'] == 'git':
            print git.Git().clone(rs['url'])


