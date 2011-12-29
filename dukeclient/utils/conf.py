# -*- coding: utf-8 -*-

import os
import yaml


def load_yaml(path):
    f = os.path.join(path) 
    try:
        return yaml.load(file(f, 'r'))
    except IOError, e:
        return False
    except yaml.YAMLError, e:
        print "Error: Could not parse configuration file:", e

CONF_TEMPLATE = """
servers:
    - name: "%(name)s"
      address: "%(server)s"
      key: "%(key)s"
"""


class ConfigManager():
    """
    This class is used to interact with configurations
    stored in ~/.duke/conf.yml in YAML format
    """

    def __init__(self):
        self.homedir = os.getenv("HOME")
        self._conf_dir = os.path.join(self.homedir, '.duke/')
        self._conf_file = os.path.join(self._conf_dir, 'conf.yml')

        if not os.path.exists(self._conf_dir):
            os.mkdir(self._conf_dir)
        if not os.path.exists(self._conf_file):
            print "Creating default configuration file:"
            self._create_config_file(name='default')
        self.conf = load_yaml(self._conf_file)

    def _create_config_file(self, name='default'):
        if name == 'default':
            address = raw_input("Server address:")
        key = raw_input("Key:")
        tpl = CONF_TEMPLATE % {
                'server': address,
                'key': key,
                'name': name,}
        try:
            f = open(self._conf_file, 'w+')
            f.write(tpl)
            f.close()
            return True
        except:
            return False

    def get_server(self, name='default'):
        """
        Returns a specified server . If no server name is provided,
        the "default" server is returned.
        """
        for p in self.conf['servers']:
            if p['name'] == name:
                return p
        return False

    def get(self, key, name='default'):
        """
        Returns a configuration value according to the provided key and server.
        If no server is specified, the "default" server is used.

        A default value can be specified. If not configuration entry match the provided
        key, the default value will be returned.

        >>> conf = ConfigManager()
        >>> conf.get('server')
        >>> dukemaster.example.com
        """
        server = self.get_server(name)
        return key in server and server[key] or None

    def set(self, key, value, server='default'):
        """
        Sets a configuration value according to the provided key and server.
        If no server is specified, the "default" server is used.

        >>> conf = ConfigManager()
        >>> conf.set('server', 'dukemaster.test.com')
        >>> conf.get('server')
        >>> dukemaster.test.com
        """
        self.conf[key] = value
        return self.conf[key]

