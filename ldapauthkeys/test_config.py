import pytest
from ldapauthkeys.config import *

def test_config():
  assertNotNull(load_config())
