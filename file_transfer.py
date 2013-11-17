def check_updates(time, auth_key):
	print "Checking server for updates"
	files = get_files(time, auth_key)
	download_files(files, auth_key)

def get_files(last_check, auth_key):
	# Dummy Code
	return []

def download_files(files, auth_key):
	# Dummy Code
	print str(len(files)) + " updates found:"
	print files
	
def file_upload(file_path):
	# Dummy Code
	print file_path + " pushed to server"
	
def file_delete(file_path):
	# Dummy Code
	print file_path + " removed from server"