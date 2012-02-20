import os, sys
import random
import shutil
import unittest
from tests import run_duke


class TestCommandInit(unittest.TestCase):
    """
    Tests for:
    duke init <projectname>
    """
    def setUp(self):
        self.tmp_dir = '/tmp/'

    def test_basic(self):
        self.assertEquals(0, 0)

if __name__ == '__main__':
    unittest.main()
