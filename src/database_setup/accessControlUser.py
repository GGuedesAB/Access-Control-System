import ctypes
import pymysql.cursors
import os
import re

# Access control system group
class acsgroup ():
    def __init__ (self, number, description):
        self.number = number
        self.description = description

    def get_number (self):
        return int(self.number)

    def get_description (self):
        return self.description

# Create root user!

# Access control system user
class acsuser ():
    def __init__ (self, name, MAC, username, password, group_number=None, user_id=None):
        self.id = user_id
        self.name = name
        self.MAC = MAC
        self.username = username
        self.encrypted_password = self.encrypt_user_info(password)
        self.group_number = group_number

    def get_id (self):
        return int(self.id)

    def get_name (self):
        return self.name

    def get_MAC (self):
        return self.MAC

    def get_username (self):
        return self.username

    def get_group_number (self):
        return int(self.group_number)

    def get_encrypted_password (self):
        return self.encrypted_password

    def encrypt_user_info (self, user_info):
        try:
            dirname = re.match('(.*\/Access-Control-System)', os.getcwd())
            dirname = dirname.group(1)
            dirname = os.path.join(dirname, 'src/encryption/encrypt.so')
            c_encrypt_ = ctypes.cdll.LoadLibrary(dirname)
            c_encrypt_.encrypt.argtype = ctypes.c_char_p
            c_encrypt_.encrypt.restype = ctypes.c_char_p
            if type(user_info) is str:
                encoded_user_info = user_info.encode('utf-8')
                encrypted_info = c_encrypt_.encrypt(encoded_user_info)
                return encrypted_info
            else:
                return None
        except OSError:
            exit(1)

# Access control system facility
class acsfacility ():
    def __init__ (self, name):
        self.name = name

    def get_name (self):
        return self.name

# Group-Facility relationship
class acsaccess ():
    def __init__ (self, group_number, facility_name):
        self.group_number = group_number
        self.facility_name = facility_name

    def get_group_number (self):
        return int(self.group_number)

    def get_facility_name (self):
        return self.facility_name