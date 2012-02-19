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
    def setUp(self):
        self.tmp_dir = '/tmp/'

    def test_basic(self):
        self.tmp_path = os.path.join(self.tmp_dir, "/tmp/test-project")

        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

        stdout, stderr, returncode = \
                run_duke('duke startproject test-project -b /tmp/')

        print stdout
        print stderr
        self.assertTrue(stdout.startswith('Created project test-project'))
        self.assertEquals(0, returncode)

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    unittest.main()
