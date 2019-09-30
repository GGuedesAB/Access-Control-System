import ctypes
import pymysql.cursors
from src.database_setup import accessControlUser

class dataBaseDriver ():

	# Checks if possible to connect to databse
	def __init__(self, host, db_owner, password, db_name):
		self.debug_mode = False
		self.host = host
		self.db_owner = db_owner
		self.password = password
		self.db_name = db_name
		try:
			conn = pymysql.connect(host=self.host, #'localhost'
								   user=self.db_owner, #'root'
								   password=self.password, #'root'
								   db=self.db_name, #'accontrol'
								   charset='utf8mb4',
							       binary_prefix=True,
								   cursorclass=pymysql.cursors.DictCursor)

		except pymysql.Error as error:
			self.DB_print(error)

		finally:
			conn.close()

	def DB_print (self, print_str):
		if self.debug_mode:
			print ('DB DEBUG: ' + str(print_str))

	def decrypt_user_info (self, acsuser_info):
		try:
			c_decrypt_ = ctypes.cdll.LoadLibrary(r"../encryption/decrypt.so")
			c_decrypt_.decrypt.argtype = ctypes.c_char_p
			c_decrypt_.decrypt.restype = ctypes.c_char_p
			if type(acsuser_info) is bytes:
				decrypted_info = c_decrypt_.decrypt(acsuser_info)
				decoded_user_info = decrypted_info.decode('utf-8')
				return decoded_user_info
			else:
				self.DB_print ('Decryption algorithm recieved not byte argument.')
		except Exception as de:
			self.DB_print ('DEC_ERROR: \n' + de)

	# groups must exist before inserting users
	def define_new_group(self, acsgroup):
		try:
			conn = pymysql.connect(host=self.host,
								   # Be careful not to confuse user from DB with 
							   	   user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
		
			with conn.cursor() as cursor:
				sql = "INSERT INTO `groups` (`number`,`description`) VALUES (%d,%s)"
				insert_tuple = (acsgroup.get_number(), acsgroup.get_description())
				result = cursor.execute(sql, insert_tuple)
				self.DB_print(result)
				conn.commit()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()

	# password must be already encrypted (bytes)
	def insert_new_user(self, acsuser):
		try:
			conn = pymysql.connect(host=self.host,
								   # Be careful not to confuse user from DB with 
							   	   user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
		
			with conn.cursor() as cursor:
				sql = "INSERT INTO `users` (`id`,`name`, `MAC`, `username`, `password`,`group_number`) VALUES (%d,%s,%s,%s,%s,%d)"
				insert_tuple = (acsuser.get_id(),acsuser.get_name(), acsuser.get_MAC(), acsuser.get_username(), acsuser.get_encrypted_password(), acsuser.get_group_number())
				result = cursor.execute(sql, insert_tuple)
				self.DB_print(result)
				conn.commit()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()

  	# facilities
	def insert_new_facility(self, acsfacility):
		try:
			conn = pymysql.connect(host=self.host,
								   # Be careful not to confuse user from DB with 
							   	   user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
		
			with conn.cursor() as cursor:
				sql = "INSERT INTO `facilities` (`name`) VALUES (%s)"
				insert_tuple = (acsfacility.get_name())
				result = cursor.execute(sql, insert_tuple)
				self.DB_print(result)
				conn.commit()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()

		# link group and facility
	def give_access(self, acsaccess):
		try:
			conn = pymysql.connect(host=self.host,
								   # Be careful not to confuse user from DB with 
							   	   user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
		
			with conn.cursor() as cursor:
				sql = "INSERT INTO `access` (`group_number`,`facility_name`) VALUES (%d,%s)"
				insert_tuple = (acsaccess.get_group_number(),acsaccess.get_facility_name())
				result = cursor.execute(sql, insert_tuple)
				self.DB_print(result)
				conn.commit()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()
	
		# User info
	def retrieve_info_from_name (self, name):
		try:
			conn = pymysql.connect(host=self.host,
							       user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
			
			with conn.cursor() as cursor:
				sql = "SELECT `id`,`name`, `MAC`, `username`,`group_number` FROM `users` WHERE `name`=%s"
				select_tuple = (name)
				cursor.execute(sql, select_tuple)
				result = cursor.fetchone()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()
			return result

		# Access info from MAC
	def check_access (self, MAC):
		try:
			conn = pymysql.connect(host=self.host,
							       user=self.db_owner,
							       password=self.password,
							       db=self.db_name,
							       charset='utf8mb4',
							       binary_prefix=True,
							       cursorclass=pymysql.cursors.DictCursor)
			
			with conn.cursor() as cursor:
				sql = "SELECT `facility_name` FROM `users`,`access` WHERE `users`.`group_number` = `access`.`group_number` AND `MAC`=%s"
				select_tuple = (MAC)
				cursor.execute(sql, select_tuple)
				result = cursor.fetchone()

		except Exception as db_error:
			self.DB_print (db_error)
			return None

		finally:
			conn.close()
			return result