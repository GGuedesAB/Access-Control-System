import ctypes
import pymysql
import logging
import uuid
import re
from src.database_setup import accessControlUser
from src.tools import logger

class mysqlConnector:
    def __init__ (self, data_base):
        self.db_logger = logger.acsLogger()
        self.db_logger.set_warning()
        self.__connect(data_base)

    def __connect(self, data_base):
        try:
            self.conn = pymysql.connect(host=data_base.host, #'localhost'
                                   user=data_base.db_owner, #'root'
                                   password=data_base.password,
                                   db=data_base.db_name, #'accontrol'
                                   charset='utf8mb4',
                                   binary_prefix=True,
                                   cursorclass=pymysql.cursors.DictCursor)
        except pymysql.OperationalError:
            self.db_logger.error('Could not connect to database ' + data_base.db_name + ' through user ' + data_base.db_owner + '@' + data_base.host)
            exit(1)

    # values must be a tuple in the same order as defined in query
    def execute_query(self, query, values):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, values)
            except pymysql.err.InternalError as internal_err:
                self.db_logger.error (internal_err.args)
                return None
            except TypeError as tperr:
                self.db_logger.error (tperr.args)
                return None
            except pymysql.err.IntegrityError as integrity_err:
                self.db_logger.error (integrity_err.args)
                return None
            else:
                query_result = cursor.fetchall()
                self.conn.commit()
                return query_result
                
    def __del__ (self):
        self.conn.close()

class dataBaseDriver:

    # checks if possible to connect to databse
    def __init__(self, host, db_owner, password, db_name):
        self.host = host
        self.db_owner = db_owner
        self.password = password
        self.db_name = db_name
        self.db_driver = mysqlConnector(self)

    def decrypt_user_info (self, acsuser_info):
        try:
            c_decrypt_ = ctypes.cdll.LoadLibrary(r"../encryption/decrypt.so")
            c_decrypt_.decrypt.argtype = ctypes.c_char_p
            c_decrypt_.decrypt.restype = ctypes.c_char_p
            if type(acsuser_info) is bytes:
                decrypted_info = c_decrypt_.decrypt(acsuser_info)
                decoded_user_info = decrypted_info.decode('utf-8')
                return decoded_user_info

        except OSError:
            exit(1)

    # groups must exist before inserting users
    def define_new_group(self, acsgroup):
        sql = "INSERT INTO `groups` (`number`,`description`) VALUES (%s,%s)"
        insert_tuple = (acsgroup.get_number(), acsgroup.get_description())
        self.db_driver.execute_query(sql, insert_tuple)
    
    # password must be already encrypted (bytes)
    def insert_new_user(self, acsuser):
        sql = "INSERT INTO `users` (`name`, `MAC`, `username`, `password`) VALUES (%s,%s,%s,%s)"
        insert_tuple = (acsuser.get_name(), acsuser.get_MAC(), acsuser.get_username(), acsuser.get_encrypted_password())
        self.db_driver.execute_query(sql, insert_tuple)

      # insert facility
    def insert_new_facility(self, acsfacility):
        sql = "INSERT INTO `facilities` (`name`) VALUES (%s)"
        insert_tuple = (acsfacility.get_name())
        self.db_driver.execute_query(sql, insert_tuple)

    # link group and facility
    def give_access(self, acsaccess):
        sql = "INSERT INTO `access` (`group_number`,`facility_name`) VALUES (%s,%s)"
        insert_tuple = (acsaccess.get_group_number(),acsaccess.get_facility_name())
        self.db_driver.execute_query(sql, insert_tuple)
    
    # user info
    def retrieve_info_from_username (self, username):
        sql = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users` WHERE `username`=%s"
        select_tuple = (username)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    # check access to facilities from MAC
    def check_access (self, MAC):
        sql = "SELECT `facility_name` FROM `users`,`access` WHERE `users`.`group_number` = `access`.`group_number` AND `MAC`=%s"
        select_tuple = (MAC)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    # password must be already encrypted (bytes)
    def add_user_info(self, acsuser):
        sql = "UPDATE `users` SET `name`=%s, `username`=%s, `password`=%s where `MAC`=%s)"
        update_tuple = (acsuser.get_name(),acsuser.get_username(), acsuser.get_encrypted_password, acsuser.get_MAC())
        self.db_driver.execute_query(sql, update_tuple)

    # admin may edit any attribute
    def edit_user(self, acsuser):
        sql = "UPDATE `users` SET `id`=%d, `name`=%s, `MAC`=%s, `username`=%s,`password`=%s, group_number=%s where `MAC`=%s)"
        update_tuple = (acsuser.get_id(),acsuser.get_name(), acsuser.get_MAC(), acsuser.get_username(), acsuser.get_encrypted_password(), acsuser.get_group_number())
        self.db_driver.execute_query(sql, update_tuple)

    # admin can remove access from a group
    def remove_access(self, acsaccess):
        sql = "DELETE FROM `access` WHERE `group_number`=%s, `facility_name`=%s"
        delete_tuple = (acsaccess.get_group_number(),acsaccess.get_facility_name())
        self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove group
    def remove_group(self, acsgroup):
        sql = "DELETE FROM `groups` WHERE `number`=%s"
        delete_tuple = (acsgroup.get_number())
        self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove user
    def remove_user(self, acsuser):
        sql = "DELETE FROM `users` WHERE `MAC`=%s OR `username=%s`"
        delete_tuple = (acsuser.get_MAC(),acsuser.get_username())
        self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove facility
    def remove_facility(self, acsfacility):
        sql = "DELETE FROM `facilities` WHERE `name`=%s"
        delete_tuple = (acsfacility.get_name())
        self.db_driver.execute_query(sql, delete_tuple)

    # change group description
    def change_group_description(self, acsgroup):
        sql = "UPDATE `groups` SET `description`=%s where `number`=%s)"
        update_tuple = (acsgroup.get_description(),acsgroup.get_number())
        self.db_driver.execute_query(sql, update_tuple)