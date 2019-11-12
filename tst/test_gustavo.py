from src.tools import logger
from src.build import build
from src.build import env_set
from src.database_setup import accessControlUser
from src.database_setup import dataBaseDriver
from src.interface import interface
from src.interface import interpreter
from src.interface import gui
from unittest import mock
import argparse
import ctypes
import unittest
import pymysql
import os
import re
import subprocess

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

class Test_build (unittest.TestCase):
    def test_supported_architecture (self):
        pass_arch1 = 'x86_64'
        pass_arch2 = 'armvl7'
        system_architecure = build._get_system_architecture()
        self.assertTrue(pass_arch1 == system_architecure or pass_arch2 == system_architecure)
    
    def test_not_supported_architecture (self):
        fail_arch = 'powerPC'
        system_architecure = build._get_system_architecture()
        self.assertNotEqual(fail_arch, system_architecure)

    def test_valid_architecture (self):
        my_architecture = build._get_system_architecture()
        if my_architecture == 'armvl7' or my_architecture == 'x86_64':
            pass_arch = build._is_architecture_supported()
            self.assertTrue(pass_arch)
        else:
            fail_arch = build._is_architecture_supported()
            self.assertFalse(fail_arch)

    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(clean=False, debug=True, verbose=False))
    def test_c_files_build(self, parser_mock):
        testing_srting = 'TestingStringEncryption'
        build.args = parser_mock.return_value
        c_build = build.make_c_files()
        encrypted_string = encrypt(testing_srting)
        decrypted_string = decrypt(encrypted_string)
        self.assertEqual(decrypted_string, testing_srting)

    @unittest.skip('Skipping cleaning .so files cause they will be needed further down the testsuite.')
    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(clean=True, debug=True, verbose=False))
    def test_clean_c_files(self, parser_mock):
        build.args = parser_mock.return_value
        c_build = build.make_c_files()
        self.assertTrue(find_shared_object('encrypt.so') is None and find_shared_object('decrypt.so') is None)

# Install database is a very hard method to test, since it envolves many calls to system.
# It would take a lot of effort to find a way to create a virtual database just for testing the method as a whole...
class Tests_intall_database (unittest.TestCase):
    @unittest.skip('Hard to test database creation.')
    def test_data_base_check(self):
        self.fail('')

class Test_env_set (unittest.TestCase):
    def test_setup_env (self):
        try:
            env_set.setup_env()
        except SystemExit:
            self.fail('System exit was called during environment variable setup.')

    def test_install_dependencies (self):
        try:
            env_set.install_python_dependencies()
        except SystemExit:
            self.fail('System exit was called during installation of dependencies.')

class Test_acsgroup (unittest.TestCase):
    def test_construction (self):
        acsgroup_instance = accessControlUser.acsgroup(5,'My bed room')
        self.assertIsInstance(acsgroup_instance, accessControlUser.acsgroup)

    def test_get_number (self):
        acsgroup_instance = accessControlUser.acsgroup(5,'My bed room')
        self.assertEqual(5, acsgroup_instance.get_number())

    def test_get_description (self):
        acsgroup_instance = accessControlUser.acsgroup(5,'My bed room')
        self.assertEqual('My bed room', acsgroup_instance.get_description())

class Test_acsuser (unittest.TestCase):
    def test_construction (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertIsInstance(acsuser_instance, accessControlUser.acsuser)

    def test_get_id (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual(35, acsuser_instance.get_id())

    def test_get_name (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual('Dummy', acsuser_instance.get_name())

    def test_get_MAC (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual('5632', acsuser_instance.get_MAC())

    def test_get_username (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual('dummy123', acsuser_instance.get_username())

    def test_get_group_number (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual(2, acsuser_instance.get_group_number())
        
    def test_get_unencrypted_password (self):
        acsuser_instance = accessControlUser.acsuser('Dummy', '5632', 'dummy123', 'glauberman', 2, 35)
        self.assertEqual('glauberman', acsuser_instance.get_unencrypted_password())

class Test_acsfacility (unittest.TestCase):
    def test_construction (self):
        acsfacility_instance = accessControlUser.acsfacility('My kitchen')
        self.assertIsInstance(acsfacility_instance, accessControlUser.acsfacility)
    
    def test_get_name (self):
        acsfacility_instance = accessControlUser.acsfacility('My kitchen')
        self.assertEqual('My kitchen', acsfacility_instance.get_name())

class Test_acsaccess (unittest.TestCase):
    def test_construction (self):
        acsaccess_instance = accessControlUser.acsaccess(21, 'My bathroom')
        self.assertIsInstance(acsaccess_instance, accessControlUser.acsaccess)

    def test_get_group_number (self):
        acsaccess_instance = accessControlUser.acsaccess(21, 'My bathroom')
        self.assertEqual(21, acsaccess_instance.get_group_number())

    def test_get_facility_name (self):
        acsaccess_instance = accessControlUser.acsaccess(21, 'My bathroom')
        self.assertEqual('My bathroom', acsaccess_instance.get_facility_name())

class Test_mysqlConnector (unittest.TestCase):
    def test_construction (self):
        database = dataBaseDriver.dataBaseDriver('localhost', 'root', 'jotaquest', 'accontrol')
        try:
            mysqlConnector_instance = dataBaseDriver.mysqlConnector(database)
        except pymysql.OperationalError:
            self.fail('Could not connect to database.')
        else:
            self.assertIsInstance(mysqlConnector_instance, dataBaseDriver.mysqlConnector)

    def test_query_execution (self):
        TEST_QUERRY = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users`"
        database = dataBaseDriver.dataBaseDriver('localhost', 'root', 'jotaquest', 'accontrol')
        try:
            mysqlConnector_instance = dataBaseDriver.mysqlConnector(database)
        except pymysql.OperationalError:
            self.fail('Could not connect to database.')
        else:
            try:
                querry_result = mysqlConnector_instance.execute_query(TEST_QUERRY)
            except:
                self.fail('Could not execute querry.')
            else:
                self.assertIsNotNone(querry_result)

class Test_gui (unittest.TestCase):
    def test_construction (self):
        my_gui = gui.GUI()
        self.assertIsNotNone(my_gui)

    def test_try_login (self):
        my_gui = gui.GUI()
        try:
            my_gui.try_login('root', 'jotaquest')
        except SystemExit:
            self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
    