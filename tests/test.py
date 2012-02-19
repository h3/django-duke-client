import os, sys
import random
import shutil
import unittest
from tests import run_duke

class TestCommandStartproject(unittest.TestCase):
    """
    Tests for: duke 
    """

    def test_basic(self):
        stdout, stderr, returncode = run_duke('duke')

        self.assertTrue(stdout.startswith('usage: duke [command] [options]'))
        self.assertEquals(1, returncode)

    def test_help(self):
        stdout, stderr, returncode = run_duke('duke -h')

        self.assertTrue(stdout.startswith('usage: duke [command] [options]'))
        self.assertEquals(1, returncode)

if __name__ == '__main__':
    unittest.main()
