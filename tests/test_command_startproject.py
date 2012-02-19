import os, sys
import random
import shutil
import unittest
from tests import run_duke


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

        self.assertTrue(stdout.startswith('Created project test-project'))
        self.assertEquals(0, returncode)

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    unittest.main()
