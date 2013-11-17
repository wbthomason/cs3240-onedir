from add_file import *
from urllib2 import HTTPError

def check_updates(time, auth_key):
	print "Checking server for updates"
	files = get_files(time, auth_key)
	download_files(files, auth_key)

def get_files(last_check, auth_key):
	# Dummy Code
	return []

def download_files(files, auth_key):
	for file in files:
        fileurl = "http://localhost:3240/%s" % file
        print "downloading file " + fileurl
        filereq = requests.get(fileurl, stream=True)
        with open(file, 'wb') as dl_file:
            for chunk in filereq.iter_content(1024):
                dl_file.write(chunk)
	
def file_upload(file_path):
	try:
		upload_file(file_path)
		print file_path + " pushed to server"
	
	except HTTPError as e:
		print e.reason()
	
def file_delete(file_path):
	# Dummy Code
	print file_path + " removed from server"