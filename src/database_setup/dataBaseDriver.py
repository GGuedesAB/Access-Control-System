import ctypes
import pymysql
import logging
import uuid
import re
import os
from src.database_setup import accessControlUser
from src.tools import logger

class mysqlConnector:
    def __init__ (self, data_base):
        self.db_logger = logger.acsLogger()
        self.db_logger.set_warning()
        self.__connect(data_base)

    def __connect(self, data_base):
        self.conn = None
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
    def execute_query(self, query, values=None):
        if self.conn is None:
            self.db_logger.error('Could not open connection to database.')
            exit (1)
        with self.conn.cursor() as cursor:
            try:
                if values is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, values)
            except pymysql.err.InternalError as internal_err:
                self.db_logger.error (internal_err.args)
            except TypeError as tperr:
                self.db_logger.error (tperr.args)
            except pymysql.err.IntegrityError as integrity_err:
                self.db_logger.error (integrity_err.args)
            except pymysql.err.OperationalError:
                self.db_logger.error ('You have no permission to make changes on accontrol.')
            except:
                self.db_logger.error ('FATAL DATABASE ERROR.')
            else:
                query_result = cursor.fetchall()
                self.conn.commit()
                return query_result
                
    def __del__ (self):
        if self.conn is not None:
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
            dirname = re.match('(.*\/Access-Control-System)', os.getcwd())
            dirname = dirname.group(1)
            dirname = os.path.join(dirname, 'src/encryption/decrypt.so')
            c_decrypt_ = ctypes.cdll.LoadLibrary(dirname)
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
        return self.db_driver.execute_query(sql, insert_tuple)
    
    # password must be already encrypted (bytes)
    def insert_new_user(self, acsuser):
        name = acsuser.get_name()
        MAC = acsuser.get_MAC()
        username = acsuser.get_username()
        unencrypted_password = acsuser.get_unencrypted_password()
        encrypted_password = acsuser.get_encrypted_password()
        sql = "INSERT INTO `users` (`name`, `MAC`, `username`, `password`) VALUES (%s,%s,%s,%s)"
        insert_tuple = (name, MAC, username, encrypted_password)
        if username is not None and username != 'root':
            try:
                create_query = 'CREATE USER \'' + username + '\'@\'localhost\' IDENTIFIED BY \'' + unencrypted_password + '\''
                privileges_query =  'GRANT SELECT ON accontrol.* TO \'' + username + '\'@\'localhost\''
                self.db_driver.execute_query(create_query)
                self.db_driver.execute_query(privileges_query)
            except pymysql.err.MySQLError:
                return None
        return self.db_driver.execute_query(sql, insert_tuple)

      # insert facility
    def insert_new_facility(self, acsfacility):
        sql = "INSERT INTO `facilities` (`name`) VALUES (%s)"
        insert_tuple = (acsfacility.get_name())
        return self.db_driver.execute_query(sql, insert_tuple)

    # link group and facility
    def give_access(self, acsaccess):
        sql = "INSERT INTO `access` (`group_number`,`facility_name`) VALUES (%s,%s)"
        insert_tuple = (acsaccess.get_group_number(),acsaccess.get_facility_name())
        return self.db_driver.execute_query(sql, insert_tuple)
    
    def retrieve_all_users (self):
        if self.db_owner != 'root':
            return None
        else:
            sql = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users`"
            result = self.db_driver.execute_query(sql)
            return result

    # user info
    def retrieve_info_from_username (self, username):
        sql = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users` WHERE `username`=%s"
        select_tuple = (username)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    def retrieve_description_from_group (self, number):
        sql = "SELECT `description` FROM `groups` WHERE `number`=%s"
        select_tuple = (number)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    # check access to facilities from MAC
    def check_access (self, MAC):
        sql = "SELECT `facility_name` FROM `users`,`access` WHERE `users`.`group_number` = `access`.`group_number` AND `MAC`=%s"
        select_tuple = (MAC)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    def retrieve_my_info (self, MAC):
        sql = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users` WHERE `MAC`=%s"
        select_tuple = (MAC)
        result = self.db_driver.execute_query(sql, select_tuple)
        return result

    # password must be already encrypted (bytes)
    def add_user_info(self, acsuser):
        username = acsuser.get_username()
        unencrypted_password = acsuser.get_unencrypted_password()
        sql = "UPDATE `users` SET `name`=%s, `username`=%s, `password`=%s where `MAC`=%s"
        update_tuple = (acsuser.get_name(),acsuser.get_username(), acsuser.get_encrypted_password(), acsuser.get_MAC())
        if username is not None and username != 'root':
            try:
                drop_query = 'DROP USER \'' + username+ '\'@\'localhost\';'
                create_query = 'CREATE USER \'' + username + '\'@\'localhost\' IDENTIFIED BY \'' + unencrypted_password + '\';'
                privileges_query =  'GRANT SELECT ON accontrol.* TO \'' + username + '\'@\'localhost\';'
                self.db_driver.execute_query(drop_query)
                self.db_driver.execute_query(create_query)
                self.db_driver.execute_query(privileges_query)
            except pymysql.err.MySQLError:
                return None
        return self.db_driver.execute_query(sql, update_tuple)

    # admin may edit any attribute
    def edit_user(self, acsuser):
        username = acsuser.get_username()
        unencrypted_password = acsuser.get_unencrypted_password()
        sql = "UPDATE `users` SET `name`=%s, `username`=%s,`password`=%s, group_number=%s where `MAC`=%s"
        update_tuple = (acsuser.get_name(), username, acsuser.get_encrypted_password(), acsuser.get_group_number(), acsuser.get_MAC())
        if username is not None and username != 'root':
            try:
                drop_query = 'DROP USER \'' + username+ '\'@\'localhost\';'
                create_query = 'CREATE USER \'' + username + '\'@\'localhost\' IDENTIFIED BY \'' + unencrypted_password + '\';'
                privileges_query =  'GRANT SELECT ON accontrol.* TO \'' + username + '\'@\'localhost\';'
                self.db_driver.execute_query(drop_query)
                self.db_driver.execute_query(create_query)
                self.db_driver.execute_query(privileges_query)
            except pymysql.err.MySQLError:
                return None
        return self.db_driver.execute_query(sql, update_tuple)

    # admin can remove access from a group
    def remove_access(self, acsaccess):
        sql = "DELETE FROM `access` WHERE `group_number`=%s AND `facility_name`=%s"
        delete_tuple = (acsaccess.get_group_number(),acsaccess.get_facility_name())
        return self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove group
    def remove_group(self, acsgroup):
        sql = "DELETE FROM `groups` WHERE `number`=%s"
        delete_tuple = (acsgroup.get_number())
        return self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove user
    def remove_user(self, acsuser):
        username = acsuser.get_username()
        MAC = acsuser.get_MAC()

        sql = "DELETE FROM `users` WHERE `MAC`=%s OR `username`=%s"
        delete_tuple = (MAC, username)
        if username is not None and username != 'root':
            try:
                drop_query = 'DROP USER \'' + username+ '\'@\'localhost\';'
                self.db_driver.execute_query(drop_query)
            except pymysql.err.MySQLError:
                return None
        return self.db_driver.execute_query(sql, delete_tuple)

    # admin can remove facility
    def remove_facility(self, acsfacility):
        sql = "DELETE FROM `facilities` WHERE `name`=%s"
        delete_tuple = (acsfacility.get_name())
        return self.db_driver.execute_query(sql, delete_tuple)

    # change group description
    def change_group_description(self, acsgroup):
        sql = "UPDATE `groups` SET `description`=%s where `number`=%s"
        update_tuple = (acsgroup.get_description(),acsgroup.get_number())
        return self.db_driver.execute_query(sql, update_tuple)