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


class GlobalConfigManager():
    """
    This class is used to interact with global configurations
    stored in ~/.duke/conf.yml in YAML format
    """

    def __init__(self):
        self.homedir = os.getenv("HOME")
        self.conf_dir = os.path.join(self.homedir, '.duke/')
        self.conf_file = os.path.join(self.conf_dir, 'conf.yml')
        self.conf = load_yaml(self.conf_file)

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

   #def _create_config_file(self, name='default'):
   #    if name == 'default':
   #        address = raw_input("Server address:")
   #    key = raw_input("Key:")
   #    tpl = GLOBAL_CONF_TEMPLATE % {
   #            'server': address,
   #            'key': key,
   #            'name': name,}
   #    try:
   #        f = open(self._conf_file, 'w+')
   #        f.write(tpl)
   #        f.close()
   #        return True
   #    except:
   #        return False


class ProjectConfigManager():
    """
    This class is used to interact with configurations
    stored in /project/.duke/conf.yml in YAML format
    """

    def __init__(self, project_path):
        self.project_path = project_path
        self.conf_file = os.path.join(self.project_path, '.duke/project_conf.yml')
        self.conf = load_yaml(self.conf_file)

    def get(self, key):
        """
        Returns a configuration value according to the provided key and server.
        If no server is specified, the "default" server is used.

        A default value can be specified. If not configuration entry match the provided
        key, the default value will be returned.

        >>> conf = ConfigManager()
        >>> conf.get('server')
        >>> dukemaster.example.com
        """
        return self.conf[key]

    def set(self, key, value):
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
