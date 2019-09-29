import ctypes
import pymysql.cursors


# Access control system group
class acsgroup ():

	def __init__ (self, number, description):
		self.debug_mode = False
		self.number = number
		self.description = description

	def ENC_print (self, print_str): #AWRAEONSODNGFOSDNFJDNFJKDNFJKNSKJ  CLASS
		if self.debug_mode:
			print ('ENC DEBUG: ' + str(print_str))

	def set_debug_mode (self): #ASIUBASIBZJSKDBZKJSBKJBEBEHZBEHBZEIHB CLASS
		self.debug_mode = True

# Access control system user
class acsuser ():

	def __init__ (self, id, name, MAC, username, password, group_number):
		self.debug_mode = False
		self.id = id
		self.name = name
		self.MAC = MAC
		self.username = username
		self.password = self.encrypt_user_info(password)
		self.group_number = group_number

	def ENC_print (self, print_str):
		if self.debug_mode:
			print ('ENC DEBUG: ' + str(print_str))

	def encrypt_user_info (self, user_info):
		try:
			c_encrypt_ = ctypes.cdll.LoadLibrary(r"/home/gustavo/Desktop/EngSoftProj/tiny-AES-c/encrypt.so") #Relative path!!!
			c_encrypt_.encrypt.argtype = ctypes.c_char_p
			c_encrypt_.encrypt.restype = ctypes.c_char_p
			if type(user_info) is str:
				encoded_user_info = user_info.encode('utf-8')
				encrypted_info = c_encrypt_.encrypt(encoded_user_info)
				return encrypted_info
			else:
				self.ENC_print ('User information is not string.')
				return None
		except Exception as ee:
			self.ENC_print (ee)

	def set_debug_mode (self):
		self.debug_mode = True

# Access control system facility
class acsfacility ():

	def __init__ (self, name):
		self.debug_mode = False
		self.name = name

	def ENC_print (self, print_str):
		if self.debug_mode:
			print ('ENC DEBUG: ' + str(print_str))

	def set_debug_mode (self):
		self.debug_mode = True

# Group-Facility relationship
class acsaccess ():

	def __init__ (self, group_number, facility_name):
		self.debug_mode = False
		self.group_number = group_number
		self.facility_name = facility_name

	def ENC_print (self, print_str):
		if self.debug_mode:
			print ('ENC DEBUG: ' + str(print_str))

	def set_debug_mode (self):
		self.debug_mode = True