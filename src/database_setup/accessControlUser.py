import ctypes
import pymysql.cursors

class acs_print():
	def __init__ (self, debug_mode=False):
		self.debug_mode = debug_mode
	
	def ENC_print (self, print_str):
		if self.debug_mode:
			print ('ENC DEBUG: ' + str(print_str))

# Access control system group
class acsgroup ():
	def __init__ (self, number, description):
		self.number = number
		self.description = description

	def get_number (self):
		return self.number

	def get_description (self):
		return self.description

# Create root user!

# Access control system user
class acsuser ():
	def __init__ (self, user_id, name, MAC, username, password, group_number, debug_mode=False):
		self.printer = acs_print(debug_mode)
		self.id = user_id
		self.name = name
		self.MAC = MAC
		self.username = username
		self.encrypted_password = self.encrypt_user_info(password)
		self.group_number = group_number

	def get_id (self):
		return self.id

	def get_name (self):
		return self.name

	def get_MAC (self):
		return self.MAC

	def get_username (self):
		return self.username

	def get_group_number (self):
		return self.group_number

	def get_encrypted_password (self):
		return self.encrypt_user_info

	def encrypt_user_info (self, user_info):
		try:
			c_encrypt_ = ctypes.cdll.LoadLibrary(r"../encryption/encrypt.so")
			c_encrypt_.encrypt.argtype = ctypes.c_char_p
			c_encrypt_.encrypt.restype = ctypes.c_char_p
			if type(user_info) is str:
				encoded_user_info = user_info.encode('utf-8')
				encrypted_info = c_encrypt_.encrypt(encoded_user_info)
				return encrypted_info
			else:
				self.printer.ENC_print ('User information is not string.')
				return None
		except Exception as ee:
			self.printer.ENC_print (ee)

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
		return self.group_number

	def get_facility_name (self):
		return self.facility_name