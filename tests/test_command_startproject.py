import os, sys
import random
import shutil
import unittest
import coverage
from tests import run_duke

#sys.path.append(os.path.realpath('../dukeclient/'))

from dukeclient.commands.startproject import StartprojectCommand

#os.environ['COVERAGE_PROCESS_START'] = 'tests/.coveragerc'
#coverage.process_startup()

class TestCommandStartproject(unittest.TestCase):
    """
    Tests for:
    duke startproject <project>
    """

    def _path_exists(self, path):
        return os.path.exists(os.path.join(self.tmp_dir, \
                self.project_name, path))

    def setUp(self):
        self.tmp_dir = '/tmp/'
        self.project_name = 'test-project'
        self.project_path = os.path.join(self.tmp_dir, self.project_name)
        if os.path.exists(self.project_path):
                shutil.rmtree(self.project_path)

    def test_args_length(self):
        self.setUp()
        stdout, stderr, returncode = run_duke('duke startproject')
        self.assertTrue(stdout.startswith('Error:'))

    def test_existing_target(self):
        self.setUp()
        StartprojectCommand().call(self.project_name, \
                base_path=self.tmp_dir, minimal=True)

        stdout, stderr, returncode = \
                run_duke('duke startproject %s -m -b %s' \
                % (self.project_name, self.tmp_dir))

        self.assertTrue(stdout.startswith('Error:'))

    def test_cli_basic(self):
        self.setUp()
        stdout, stderr, returncode = \
                run_duke('duke startproject %s -b %s' \
                % (self.project_name, self.tmp_dir))

        self.assertTrue(stdout.startswith('Created project %s' \
                % self.project_name))
        self.assertEquals(0, returncode)
        self.assertTrue(self._path_exists('setup.py'))
        self.assertTrue(self._path_exists('README.rst'))
        self.assertTrue(self._path_exists('LICENSE'))

    def test_cli_minimal(self):
        self.setUp()
        stdout, stderr, returncode = \
                run_duke('duke startproject %s -m -b %s' \
                % (self.project_name, self.tmp_dir))

        self.assertTrue(stdout.startswith('Created project %s' \
                % self.project_name))
        self.assertEquals(0, returncode)
        self.assertTrue(self._path_exists('setup.py'))
        self.assertFalse(self._path_exists('README.rst'))
        self.assertFalse(self._path_exists('LICENSE'))

    def test_api_basic(self):
        self.setUp()
        StartprojectCommand().call(self.project_name, base_path=self.tmp_dir)

        self.assertTrue(self._path_exists('setup.py'))
        self.assertTrue(self._path_exists('README.rst'))
        self.assertTrue(self._path_exists('LICENSE'))

    def test_api_minimal(self):
        self.setUp()
        StartprojectCommand().call(self.project_name, \
                base_path=self.tmp_dir, minimal=True)

        self.assertTrue(self._path_exists('setup.py'))
        self.assertFalse(self._path_exists('README.rst'))
        self.assertFalse(self._path_exists('LICENSE'))

    def tearDown(self):
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)

if __name__ == '__main__':
    unittest.main()
