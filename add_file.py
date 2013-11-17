from twisted.web import client

import requests
import db_access
import MySQLdb as mdb
import sys


def upload_file(File):
    url = 'http://localhost:3240'
    files = {'file': open(File)}
    req = requests.put(url, files=files)
    req.raise_for_status()

if __name__ == "__main__":
    file_to_upload = raw_input("File to upload?")
    try:
        if db_access.login("knox.dru@gmail.com", "password"):
            upload_file(file_to_upload)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)