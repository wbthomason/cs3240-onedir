import sys

import requests
import MySQLdb as mdb


def upload_file(file_name, user):
    url = 'http://localhost:3240/files'
    files = {'file': open(file_name)}
    params = {'filename': file_name[len(user.dir):], 'username': user.email}
    req = requests.put(url, files=files, params=params)
    req.raise_for_status()

if __name__ == "__main__":
    file_to_upload = raw_input("File to upload? ")
    try:
        upload_file(file_to_upload, 'test1')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)