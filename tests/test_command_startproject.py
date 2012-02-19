import os, sys
import random
import shutil
import unittest
import subprocess


def run_duke(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return (stdout, stderr, proc.returncode)


class TestCommandStartproject(unittest.TestCase):
    """
    Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})
    """
    def setUp(self):
        self.tmp_dir = '/tmp/'

    def test_basic(self):
        self.tmp_path = os.path.join(self.tmp_dir, "/tmp/test-project")

        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

        stdout, stderr, returncode = run_duke('duke startproject test-project -b /tmp/')
        self.assertTrue(stdout.startswith('Created project test-project'))
        self.assertEquals(0, returncode)

    def tearDown(self):
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)

if __name__ == '__main__':
    unittest.main()

