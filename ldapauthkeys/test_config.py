import unittest
from ldapauthkeys.config import *

class TestMyCode(unittest.TestCase):
  def test_config(self):
    self.assertNotNull(load_config())
