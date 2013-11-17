class User():
	def __init__(self, email, password):
		self.email = email
		self.password = password
		self.auth_key = None

	def login(self):
		# Dummy Code
		self.auth_key = 0
		return True
	
	def logout(self):
		self.auth_key = None
		return True