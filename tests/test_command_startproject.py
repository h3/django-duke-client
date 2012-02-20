import os, sys
import random
import shutil
import unittest
import coverage
from tests import run_duke

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

    def test_basic(self):
        self.tmp_path = os.path.join(self.tmp_dir, self.project_name)

        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

        stdout, stderr, returncode = \
                run_duke('duke startproject test-project -b %s' % self.tmp_dir)

        self.assertTrue(stdout.startswith('Created project %s' % self.project_name))
        self.assertEquals(0, returncode)
        self.assertTrue(self._path_exists('setup.py'))
        self.assertTrue(self._path_exists('README.rst'))
        self.assertTrue(self._path_exists('LICENSE'))

    def test_minimal(self):
        self.tmp_path = os.path.join(self.tmp_dir, self.project_name)

        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

        stdout, stderr, returncode = \
                run_duke('duke startproject test-project -b %s' % self.tmp_dir)

        self.assertTrue(stdout.startswith('Created project %s' % self.project_name))
        self.assertEquals(0, returncode)
        self.assertTrue(os.path.exists(os.path.join(self.tmp_dir, self.project_name, 'setup.py')))

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    unittest.main()
