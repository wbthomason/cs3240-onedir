from add_file import *
from urllib2 import HTTPError
import requests

def check_updates(time, user):
	print "Checking server for updates"
	files = get_files(time, user)
	download_files(files, user)

def get_files(last_check, user):
	url = "http://localhost:3240/check/"
	args = {'email':user.email, 'last_check':last_check}
	r = requests.get(url, params=args)
	files = json.loads( r.text() )['files']
	
	return files

def download_files(files, user):
	for file in files:
        fileurl = "http://localhost:3240/files/%s" % file
        print "downloading file " + fileurl
        filereq = requests.get(fileurl, stream=True)
        local_file = user.dir + file
        with open(local_file, 'wb') as dl_file:
            for chunk in filereq.iter_content(1024):
                dl_file.write(chunk)
	
def file_upload(file_path, user):
	try:
		upload_file(file_path, user)
		print file_path + " pushed to server"
	
	except HTTPError as e:
		print e.reason()
	
def file_delete(file_path, user):
	# Dummy Code
	print file_path + " removed from server"