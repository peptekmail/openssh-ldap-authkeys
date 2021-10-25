import unittest
from ldapauthkeys.config import *
from ldapauthkeys.util import *
import glob
import os

class TestMyCode(unittest.TestCase):
  def test_cert_to_sshkey(self):
    list_of_files = glob.glob('/usr/share/ca-certificates/mozilla/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    f = open(latest_file,'rb')
    self.assertIsNot(cert_to_sshkey(f.read()),'')
    f.close()
    
  def test_der_cert_to_sshkey(self):
    f = open('certificate.der','rb')
    self.assertIsNot(cert_to_sshkey(f.read()),'')
    f.close()
    
  def test_config(self):
    self.assertNotEqual(load_config(), None)
