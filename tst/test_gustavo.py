from src.tools import logger
from src.build import build
from unittest import mock
import argparse
import ctypes
import unittest
import os
import re
import subprocess

#For now, this test must be run from within src/build

def find_shared_object (shared_object_name):
    base_dirname = re.match('(.*\/Access-Control-System)', os.getcwd())
    base_dirname = base_dirname.group(1)
    dirname = os.path.join(base_dirname, 'src/encryption/', shared_object_name)
    if os.path.exists(dirname):
        return dirname
    else:
        return None

def encrypt (string_to_encrypt):
    shared_object = find_shared_object('encrypt.so')
    c_encrypt_ = ctypes.cdll.LoadLibrary(shared_object)
    c_encrypt_.encrypt.argtype = ctypes.c_char_p
    c_encrypt_.encrypt.restype = ctypes.c_char_p
    encoded_string = string_to_encrypt.encode('utf-8')
    encrypted_string = c_encrypt_.encrypt(encoded_string)
    return encrypted_string

def decrypt (string_to_decrypt):
    shard_object = find_shared_object('decrypt.so')
    c_decrypt_ = ctypes.cdll.LoadLibrary(shard_object)
    c_decrypt_.decrypt.argtype = ctypes.c_char_p
    c_decrypt_.decrypt.restype = ctypes.c_char_p
    decrypted_string = c_decrypt_.decrypt(string_to_decrypt)
    decoded_string = decrypted_string.decode('utf-8')
    return decoded_string

class Test_get_system_architecture (unittest.TestCase):
    def test_supported_architecture (self):
        pass_arch1 = 'x86_64'
        pass_arch2 = 'armvl7'
        system_architecure = build._get_system_architecture()
        self.assertTrue(pass_arch1 == system_architecure or pass_arch2 == system_architecure)
    
    def test_not_supported_architecture (self):
        fail_arch = 'powerPC'
        system_architecure = build._get_system_architecture()
        self.assertNotEqual(fail_arch, system_architecure)

class Test_is_architecture_supported (unittest.TestCase):
    def test_valid_architecture (self):
        my_architecture = build._get_system_architecture()
        if my_architecture == 'armvl7' or my_architecture == 'x86_64':
            pass_arch = build._is_architecture_supported()
            self.assertTrue(pass_arch)
        else:
            fail_arch = build._is_architecture_supported()
            self.assertFalse(fail_arch)
    
# I don't know how to test apt packages installation method

#class Test_call_std_subprocess (unittest.TestCase):  
#    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(clean=False, debug=True, verbose=False))
#    def test_fail_subprocess (self):
#        build.args = build.arg_parser()
#        self.assertRaises(subprocess.CalledProcessError, build._call_std_subprocess, ['ping'])

class Test_make_c_files (unittest.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(clean=False, debug=True, verbose=False))
    def test_c_files_build(self, parser_mock):
        testing_srting = 'TestingStringEncryption'
        build.args = parser_mock.return_value
        c_build = build.make_c_files()
        encrypted_string = encrypt(testing_srting)
        decrypted_string = decrypt(encrypted_string)
        self.assertEqual(decrypted_string, testing_srting)

    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(clean=True, debug=True, verbose=False))
    def test_clean_c_files(self, parser_mock):
        build.args = parser_mock.return_value
        c_build = build.make_c_files()
        if find_shared_object('encrypt.so') is None and find_shared_object('decrypt.so') is None:
            self.assertEqual(1,1)
        else:
            self.assertEqual(0,1)

class Test_check_folder (unittest.TestCase):
    def test_run_from_folder(self):
        try:
            builder = build.check_folder()
        except SystemExit:
            self.fail()


if __name__ == "__main__":
    unittest.main()
    