import os, sys
import random
import shutil
import unittest
from tests import run


class TestCommandInit(unittest.TestCase):
    """
    Tests for:
    duke init <projectname>
    """

    def _path_exists(self, path):
        # Check if a file exists within the root directory of the project.
        return os.path.exists(os.path.join(self.tmp_dir, \
                self.project_name, path))

    def setUp(self):
        self.tmp_dir = '/tmp/'
        self.project_name = 'test-project'
        self.django_project_name = 'testproject'
        self.project_path = os.path.join(self.tmp_dir, self.project_name)
        if os.path.exists(self.project_path):
                shutil.rmtree(self.project_path)

        run('duke startproject %s -m -b %s' \
                % (self.project_name, self.tmp_dir))

    def test_args_length(self):
        self.setUp()
        stdout, stderr, returncode = run('duke init')
        self.assertEquals(1, returncode)
        self.assertTrue(stdout.startswith('Error:'))

    def test_initialize(self):
        self.setUp()
        stdout, stderr, returncode = \
                run('duke init %s -n -b %s' % \
                (self.django_project_name, self.project_path))

        self.assertEquals(0, returncode)
        self.assertTrue(self._path_exists('bootstrap.py'))
        self.assertTrue(self._path_exists('buildout.cfg'))
        self.assertTrue(self._path_exists('dev.cfg'))
        self.assertTrue(self._path_exists('.duke/'))
        self.assertTrue(self._path_exists('.duke/base.cfg'))
        self.assertTrue(self._path_exists('.duke/bin/dev'))
        self.assertTrue(self._path_exists('.duke/bin/env'))
        self.assertTrue(self._path_exists('.duke/bin/profile'))
        

    def tearDown(self):
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)

if __name__ == '__main__':
    unittest.main()
